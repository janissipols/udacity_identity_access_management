/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://5000-cs-454817659072-default.cs-europe-west4-pear.cloudshell.dev/', // the running FLASK api server url
  auth0: {
    url: 'dev-isajo81nbmm8nfy8.us', // the auth0 domain prefix
    audience: 'dev', // the audience set for the auth0 app
    clientId: 'Tf0aDi9z2JlciiqrqnWN4lpDEB00cLep', // the client id generated for the auth0 app
    callbackURL: 'https://8100-cs-454817659072-default.cs-europe-west4-pear.cloudshell.dev', // the base url of the running ionic application. 
  }
};
