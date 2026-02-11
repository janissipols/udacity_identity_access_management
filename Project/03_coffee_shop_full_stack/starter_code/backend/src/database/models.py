import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app): # Binds a Flask application and a SQLAlchemy service.
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all(): # Drops existing database tables, creates new ones, and populates with sample data.
    db.drop_all()
    db.create_all()

    drink1 = Drink(
        title='matcha shake',
        recipe='[{"name": "milk", "color": "grey", "parts": 1}, {"name": "matcha", "color": "green", "parts": 3}]'
    )

    drink2 = Drink(
        title='flatwhite',
        recipe='[{"name": "milk", "color": "grey", "parts": 3}, {"name": "coffee", "color": "brown", "parts": 1}]'
    )

    drink3 = Drink(
        title='cap',
        recipe='[{"name": "foam", "color": "white", "parts": 1}, {"name": "milk", "color": "grey", "parts": 2}, {"name": "coffee", "color": "brown", "parts": 1}]'
    )

    drink1.insert()
    drink2.insert()
    drink3.insert()

class Drink(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)

    def short(self): # Returns a short form representation of the drink model.
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self): # Returns a long form representation of the drink model.
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self): # Inserts a new drink model into the database.
        db.session.add(self)
        db.session.commit()

    def delete(self): # Deletes a drink model from the database.
        db.session.delete(self)
        db.session.commit()

    def update(self): # Updates an existing drink model in the database.
        db.session.commit()

    def __repr__(self): # Returns a string representation of the drink.
        return json.dumps(self.short())