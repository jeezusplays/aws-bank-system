// Access environment variables
const AWS_LOGIN_DOMAIN = process.env.VUE_APP_AWS_LOGIN_DOMAIN;
const CLIENT_ID = process.env.VUE_APP_CLIENT_ID;
const REDIRECT_URL = process.env.VUE_APP_REDIRECT_URL;
const LOGIN_URL = "https://" + AWS_LOGIN_DOMAIN + "/login?response_type=code&client_id="+CLIENT_ID+"&redirect_uri="+REDIRECT_URL;

// Export the variables
export {
  LOGIN_URL
}

