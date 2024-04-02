const config = {
    Auth: {
      Cognito: {
        userPoolClientId: process.env.VUE_APP_CLIENT_ID,
        userPoolId: process.env.VUE_APP_USER_POOL_ID,
        loginWith: { // Optional
          oauth: {
            domain: "https://"+process.env.VUE_APP_AWS_LOGIN_DOMAIN,
            scopes: ['openid email phone profile'],
            redirectSignIn: ['http://localhost:8080/dashboard'],
            responseType: 'code'
          }
        }
      }
    }
  }
// export default Amplify;

export { config };
