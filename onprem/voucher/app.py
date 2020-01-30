from flask import Flask, request, Response, jsonify, abort
import jwt
import os
import requests
from datetime import datetime
from datetime import timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dsa, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key


app = Flask(__name__)

with open(os.getenv('JWT_PUBLIC_KEY_PATH'), "r") as f:
    public_key = f.read()

with open(os.getenv('JWT_PRIVATE_KEY_PATH'), "r") as f:
    private_key = f.read()


def extract_access_token(r):
    access_token = None
    if 'Authentication' in request.headers:
        authentication = r.headers.get('Authentication')
        app.logger.warning('Authentication in header')
        authentication = authentication.split(' ')
        if len(authentication) != 2:
            app.logger.warning('len(authentication) != 2')
            abort(401)
        if authentication[0].lower() != 'bearer':
            app.logger.warning('no bearer')
            abort(401)
        access_token = authentication[1]
    elif 'access_token' in r.cookies:
        app.logger.warning('checking for access_token in cookies')
        access_token = r.cookies.get('access_token')
    if not access_token:
        app.logger.warning('No access token found in cookie or header')
        abort(401, "No access token found in cookie or header")
    return access_token

def get_access_token(request):
    # app.logger.warning(request.url)
    app.logger.warning(request.headers)
    # app.logger.warning(request.args)
    # app.logger.warning('calling fence')
    # response = requests.get('http://fence-service/user/anyaccess', headers=request.headers)
    url = 'http://arborist-service/auth/mapping'
    response = requests.get(url, headers=request.headers)
    # app.logger.warning(response.status_code)
    # app.logger.warning(response.text)
    # app.logger.warning(response.headers)

    if not response.status_code == 200:
        app.logger.warning(f'{url} did not return 200 {response.status_code}')
        abort(response.status_code, f'{url} did not return 200 {response.status_code}')

    access_token = extract_access_token(request)

    try:
        access_token = jwt.decode(access_token, public_key, audience='data')  # credentials ?
    except Exception as e:
        app.logger.warning(f"Could not decode access_token {str(e)}")
        abort(401, f"Could not decode access_token {str(e)}")

    app.logger.debug(f"decoded token")
    app.logger.debug(access_token)
    return access_token


@app.route("/auth")
def nginx_auth():
    access_token = get_access_token(request)
    user_name = access_token['context']['user']['name']
    roles = []
    if access_token['context']['user']['is_admin']:
        roles.append('admin')
    for p in access_token['context']['user']['projects']:
        for role in access_token['context']['user']['projects'][p]:
            roles.append(f'{p}-{role}')
    encoded_jwt = jwt.encode({'user_name': user_name, 'roles': roles}, private_key, algorithm='RS256').decode('UTF-8')
    my_response = jsonify({'message': 'Authenticated'})
    my_response.headers['Authorization'] = f"Bearer {encoded_jwt}"
    return my_response


@app.route("/user")
def user():
    app.logger.warning(request.url)
    access_token = extract_access_token(request)
    access_token = jwt.decode(access_token, verify=False)
    return jsonify({'message': access_token})


@app.route("/remote-user")
def remote_user():
    app.logger.warning(request.url)
    app.logger.warning(request.headers)
    remote_user = request.headers.get('Remote-User')
    remote_roles = request.headers.get('Remote-Roles')
    return jsonify({'Remote-User': remote_user, 'Remote-Roles': remote_roles})
