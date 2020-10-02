# Oauth2.0-demo
To demonstrate OIDC authentication with authorization code grant type
API authentication using the authorization grant type is the most secure type of authentication as it involves a 
two-way communication.
- One is to the authorization endpoint to generate auth code where user enters his credentials
- Second is to the authorization server where the token endpoint is used to generate tokens
- This ensures that it is almost impossible for external forces to intercept the APIs 

## How to use?
- Run the script `app.py` which acts like a local standalone server
- Prefill the details in the `config.json`
    1. client ID and client secret of the application
    2. redirect uri
    3. Authorization endpoint, which will generate the authorization code
    4. Token endpoint, which inturn will generate access and identity tokens
The access and identity tokens generated from the authorization server(can be an Apigee proxy) will 
expire in a few minutes, hence the subsequent API calls will fail to authenticate. To regenerate access or 
identity tokens, a call to the authorization endpoint is needed which will generate the auth code. This auth code
will be further used by token endpoints to generate the tokens.

## Refresh tokens
To solve this issue, refresh tokens are generated which eliminates the step to generate authorization code
by calling the authorization endpoint. Instead the token endpoint is called with `grant_type` as `refresh_token`

The refresh tokens can be generated over regular intervals by only using the token endpoints.

## Authorization code
![Access token](sample_images/authCode.PNG?raw=true "Authorization code") 

## Access and ID token
![Access token](sample_images/access_ID_token.PNG?raw=true "Access token") 

## Refresh token
![Refresh token](sample_images/refreshToken.PNG?raw=true "Refresh token") 