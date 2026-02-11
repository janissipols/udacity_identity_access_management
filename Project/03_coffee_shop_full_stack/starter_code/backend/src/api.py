import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

db_drop_and_create_all()

# GET /drinks
# Retrieves a list of drinks in short format.
@app.route('/drinks')
def get_drinks(): # Retrieves a list of drinks in short format.
    drinks = Drink.query.order_by(Drink.id).all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    })


# GET /drinks-detail
# Retrieves a list of drinks in detailed format, requires 'get:drinks-detail' permission.
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload): # Retrieves a list of drinks in detailed format, requires 'get:drinks-detail' permission.
    drinks = Drink.query.order_by(Drink.id).all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    })


# POST /drinks
# Creates a new drink, requires 'post:drinks' permission.
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload): # Creates a new drink, requires 'post:drinks' permission.
    body = request.get_json()
    if body is None:
        abort(400)
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    if title is None or recipe is None:
        abort(422)
    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


# PATCH /drinks/<id>
# Updates an existing drink, requires 'patch:drinks' permission.
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id): # Updates an existing drink, requires 'patch:drinks' permission.
    body = request.get_json()
    if body is None:
        abort(400)

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title is not None:
        drink.title = title
    if recipe is not None:
        drink.recipe = json.dumps(recipe)
    try:
        drink.update()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


# DELETE /drinks/<id>
# Deletes a drink, requires 'delete:drinks' permission.
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id): # Deletes a drink, requires 'delete:drinks' permission.
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'delete': id
    })


@app.errorhandler(422)
def unprocessable(error): # Handles 422 unprocessable entity errors.
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error): # Handles 404 resource not found errors.
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(ex): # Handles authentication errors.
    return jsonify({
        "success": False,
        "error": ex.status_code,
        "message": ex.error['description']
    }), ex.status_code
