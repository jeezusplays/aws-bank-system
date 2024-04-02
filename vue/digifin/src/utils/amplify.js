import { fetchAuthSession } from 'aws-amplify/auth';

const config = {
    Auth: {
      Cognito: {
        userPoolClientId: import.meta.env.VITE_CLIENT_ID,
        userPoolId: import.meta.env.VITE_USER_POOL_ID,
        loginWith: { // Optional
          oauth: {
            domain: "https://"+import.meta.env.VITE_AWS_LOGIN_DOMAIN,
            scopes: ['openid email phone profile'],
            redirectSignIn: ['http://localhost:8080/dashboard'],
            responseType: 'code'
          }
        }
      }
    }
  }

async function currentSession() {
  try {
    const { accessToken, idToken } = (await fetchAuthSession()).tokens ?? {};
    return { accessToken, idToken };
  } catch (err) {
    console.log(err);
    throw err;
  }
}

export { config, currentSession };
