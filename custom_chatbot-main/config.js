const dotenv = require('dotenv');
dotenv.config();
module.exports = {
    tenantId: process.env.APPID_TENANT_ID,
    clientId: process.env.APPID_CLIENT_ID,
    secret: process.env.APPID_SECRET,
    oauthServerUrl: process.env.APPID_OAUTH_SERVER_URL,
    redirectUri: process.env.APPID_REDIRECT_URI,
    fileupload_endpoint: process.env.FILEUPLOAD_ENDPOINT,
    port: process.env.PORT
};


