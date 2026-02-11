export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-isajo81nbmm8nfy8.us', // the auth0 domain prefix
    audience: 'dev', // the audience set for the auth0 app
    clientId: 'Tf0aDi9z2JlciiqrqnWN4lpDEB00cLep', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
