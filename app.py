import flask
import requests
import json
import constants

app = flask.Flask(__name__)

with open('config.json') as f:
  config_data = json.load(f)

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/authorize')
def authorize():
    input_parameters = {constants.CLIENT_ID: config_data[constants.CLIENT_ID],
                        "response_type": "code",
                        "scope": "openid profile email offline_access",
                        constants.REDIRECT_URI: config_data[constants.REDIRECT_URI]}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    authorize_response = requests.post(url=config_data[constants.AUTHORIZATION_URL], data=input_parameters,
                                       headers=headers)
    # print(authorize_response, dir(authorize_response))

    return authorize_response.text

@app.route('/callback')
def call():
    code = flask.request.args.get(constants.CODE, "")
    # send request to token URL to get access token
    input_parameters = {constants.CLIENT_ID: config_data[constants.CLIENT_ID],
                        constants.CLIENT_SECRET: config_data[constants.CLIENT_SECRET],
                        constants.GRANT_TYPE: config_data[constants.GRANT_TYPE_AUTH_CODE],
                        constants.CODE: code,
                        constants.REDIRECT_URI: config_data[constants.REDIRECT_URI]}
    response_data = requests.get(url=config_data[constants.TOKEN_URL], data=input_parameters)
    token_resp = json.loads(response_data.text)

    refresh_input = {constants.CLIENT_ID: config_data[constants.CLIENT_ID],
                     constants.CLIENT_SECRET: config_data[constants.CLIENT_SECRET],
                     constants.GRANT_TYPE: config_data[constants.GRANT_TYPE_REFRESH],
                     config_data[constants.GRANT_TYPE_REFRESH]: token_resp[config_data[constants.GRANT_TYPE_REFRESH]]
                     }
    resp_data = requests.get(url=config_data[constants.TOKEN_URL], data=refresh_input)
    refresh_data = json.loads(resp_data.text)
    return flask.jsonify({"auth_code": code, "token_resp": token_resp, 'refresh_token': refresh_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)