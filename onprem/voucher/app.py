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

wiki_certs = {"jwk":{"kty":"RSA","n":"u6RPmiWR9VHeiqeoJdDdwwwibOW50NlG6TNGUKA6I9OIv48yy6H0k1-M7yQCyvJMjLI3AZ0Fzb0hoFk8xObv0nSaJ3CB1eZEbqNXt_X7l8YpdVXlvTj7yp8hWmaKaGYE7o_utfWySn1763n6NDYJ8ZmRkVajMVrlq5KsWCEQ2NHkABIIAN1gNXEbCcOniP4kweXHiWn7wm3Bcg85G2XaumYx0grRtV4kUdfrpUjSkcnnIqCbzjyzxuLjN3XNitCTKvVlnJsndWYeAam2NkNT9uCHN1c0iBEslApXPnVMk4Bn-D0ZokMi4TU0VWy1but-mdZzL_r2bidnyzBs-f_k_w","e":"AQAB"},"public":"-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAu6RPmiWR9VHeiqeoJdDdwwwibOW50NlG6TNGUKA6I9OIv48yy6H0\nk1+M7yQCyvJMjLI3AZ0Fzb0hoFk8xObv0nSaJ3CB1eZEbqNXt/X7l8YpdVXlvTj7\nyp8hWmaKaGYE7o/utfWySn1763n6NDYJ8ZmRkVajMVrlq5KsWCEQ2NHkABIIAN1g\nNXEbCcOniP4kweXHiWn7wm3Bcg85G2XaumYx0grRtV4kUdfrpUjSkcnnIqCbzjyz\nxuLjN3XNitCTKvVlnJsndWYeAam2NkNT9uCHN1c0iBEslApXPnVMk4Bn+D0ZokMi\n4TU0VWy1but+mdZzL/r2bidnyzBs+f/k/wIDAQAB\n-----END RSA PUBLIC KEY-----\n","private":"-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256CBC,C9107DCFBC394EEB852AE4A052F22B7D\n\n3IfPBSllZrIi2lftcTpd/hLMWNB4kGDECvPpodRGBA2XU9UJKPZmhDPygCrSSGGC\n0lfHlblu+m6PJxSOIJYZ2jZ4Ue5z8o12eWF6DwsEU8T74BJuv1L3t5NMkxHvvzwW\nU7NYsz06FUEU1LOi9MQS3Ywgx0OsSa7U0xuW/NlyVbahlQj4RZN/KxjrSdGrhZ90\nspunaodgsLvz/daaoXZbgVNRMUb43baoU6Dmo8qqP+PkSJe2pnVtbRqE58UAYyqT\n9aDCKq8yF8T5ZR/wxYGuzgs9isY4hDXTzrCWg6XVhzb5y4ExddiIrMh04R+BsR2Z\nb69FFts15hGV4p6IwFjhalNirUZQnxeyBD7EAjkUtN20RNEWjn3iiIx1e8bUQ6r4\n9FWqHAOawsqpDy2g5CdtK7jS43cebBmuCbl/1LuZ2m/siKvd+FA+PNtrB06OtY/\nSEpHqAyfRVA/QL71IJn8/0NkSlNXn5L0zifepTtBmAcLOuRWb02kSFDyXsQFOfLy\nzZL29pujmnKcfeu0uJv4o9rihL3u/kWS+nZMS7E/8zsjoLnRGDSASF8MvgimzV41\nlDODEGmJdnpY4BEVzWiOWKJ/NJ7OFFEO8S3FWSl8JgnHUlPVsSdLNxrefIN1cJim\nnk2Cc+CcaTBnytbG94ogRlAu4Vb4Fhn5+pUJZH9QcFUMOW0MVG5gbqmE3XVsXZjW\n9rb0WfnTBOUhU2kgKXLtFBdVXkp32iiK/J1tg//uJgKi4CoRdgGX0o7BpE9mI5Bw\nAzlz/IZ580+i2rc6Ns6/ncHR/i67OQY9/3/C4VXB3QBfnZh4WNnyvIQiAHeF7299\nkcNR9sLW+OVMUjWeAcH2viFZ+8ooxtuFB8zNs35VjpDngm3vlDsdeQlt5WxGrfLT\nfqmhcANL8KPPNWuXVYDRZJSzEeE+hfG5IJWEeOGmHvPgLxoVpD6sYC0FSQEx/Dc\nL9Kfe9COaPR0Dov6m+qcXBixLW1Vja/wGYKd6NEiJEHYSPNF5jSxVE9tdXHxIb2Q\n6yZUtOuWTqD5uRWT4IX0W3jl2JwF1RAwroVDVGnoIUzTvB/fKj11SmVYOrFRumh7\nAY2WjD5WimbxJnVOSiWNr318vdCzAoFELBzUC6JNFm3Q5VTrET0toUEycivGGQLV\nps5NBvcffO0cqL3yO38UBBktW34IDnTdPcbXlDaD1HAApSG4fEziFfDb6YEkwZhe\n7KMHDgiUQFM1ao916Tcxtg+OsFCso6c6yu1h3y+NqiIxyLYU+nJUPqHJSLekEWCr\nOJC3LQXSZR9Lz6+HqpovO1/U/7JHRgM5UliyN63x6Ybozn5UFooP+m6ZniJ2qINk\nLQupUD/fzKGxivCtkwtqDNystXQadWJZQTW/ORECaVCBnVkRzHRc4t4nxE1k8akz\nwaqm3WLwVLSwgx0O/m2dtBk1gb7aOdbeYyMKSIK3pa52xx2qEazw5/3luwIPUb2W\nBmIHddPmFmKvzr3gVim4LcB+M4vbdaxSC+wB9nvQ8L5VgBz7BW8yoQwVvvhI1mZ6\n9msuQJCDX90lBy2bl1IwcwO9gR3IWjVl4rF7frnXiB/gK/yFWOs6RnGqFFCBrYSm\n-----END RSA PRIVATE KEY-----\n"}


wiki_secret = "b50f20431a6649a0e8fab7810116b3615334ed37e1428bbcb984dc60c5d0f020"

def extract_access_token(r):
    access_token = None
    if 'Authorization' in request.headers:
        authorization = r.headers.get('Authorization')
        app.logger.warning('Authorization in header')
        authorization = authorization.split(' ')
        if len(authorization) != 2:
            app.logger.warning('len(authorization) != 2')
            return abort(401)
        if authorization[0].lower() != 'bearer':
            app.logger.warning('no bearer')
            return abort(401)
        access_token = authorization[1]
    elif 'access_token' in r.cookies:
        access_token = r.cookies.get('access_token')
        app.logger.warning('access_token in header')
    if not access_token:
        app.logger.warning('No access token found in cookie or header')
        return abort(401, "No access token found in cookie or header")
    return access_token

def get_access_token(request):
    app.logger.warning(request.url)
    app.logger.warning(request.headers)
    app.logger.warning(request.args)
    app.logger.warning('calling fence')
    response = requests.get('http://fence-service/user/anyaccess', headers=request.headers)
    app.logger.warning(response.status_code)
    app.logger.warning(response.text)
    app.logger.warning(response.headers)

    if not response.status_code == 200:
        my_response = jsonify({'message': 'Authentication failed'})
        my_response.status_code = response.status_code
        app.logger.warning(f'http://fence-service/user/anyaccess did not return 200 {response.status_code}')
        return my_response

    access_token = extract_access_token(request)

    try:
        access_token = jwt.decode(access_token, public_key, audience='credentials')
    except Exception as e:
        app.logger.warning(f"Could not decode access_token {str(e)}")
        return abort(401, f"Could not decode access_token {str(e)}")

    app.logger.warning(f"decoded token")
    app.logger.warning(access_token)
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

@app.route("/wiki-auth")
def wiki_token():
    # setup claims for wiki token,
    claims = {
      "id": 1,
      "email": "walsbr@ohsu.edu",
      "name": "Administrator",
      "pictureUrl": None,
      "timezone": "America/New_York",
      "localeCode": "en",
      "defaultEditor": "markdown",
      "permissions": [
        "manage:system"
      ],
      "groups": [
        1
      ],
      "iat": datetime.utcnow(),
      "exp": datetime.utcnow() + timedelta(seconds=2100),
      "aud": "urn:wiki.js",
      "iss": "urn:wiki.js"
    }


    # wiki_private_key_decrypted = load_pem_private_key(str.encode(wiki_private_key), password=str.encode(wiki_secret), backend=default_backend())
    secret = "-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256CBC,C9107DCFBC394EEB852AE4A052F22B7D\n\n3IfPBSllZrIi2lftcTpd/hLMWNB4kGDECvPpodRGBA2XU9UJKPZmhDPygCrSSGGC\n0lfHlblu+m6PJxSOIJYZ2jZ4Ue5z8o12eWF6DwsEU8T74BJuv1L3t5NMkxHvvzwW\nU7NYsz06FUEU1LOi9MQS3Ywgx0OsSa7U0xuW/NlyVbahlQj4RZN/KxjrSdGrhZ90\nspunaodgsLvz/daaoXZbgVNRMUb43baoU6Dmo8qqP+PkSJe2pnVtbRqE58UAYyqT\n9aDCKq8yF8T5ZR/wxYGuzgs9isY4hDXTzrCWg6XVhzb5y4ExddiIrMh04R+BsR2Z\nb69FFts15hGV4p6IwFjhalNirUZQnxeyBD7EAjkUtN20RNEWjn3iiIx1e8bUQ6r4\n9FWqHAOawsqpDy2g5CdtK7jS43cebBmuCbl/1LuZ2m/siKvd+FA+PNtrB06OtY/\nSEpHqAyfRVA/QL71IJn8/0NkSlNXn5L0zifepTtBmAcLOuRWb02kSFDyXsQFOfLy\nzZL29pujmnKcfeu0uJv4o9rihL3u/kWS+nZMS7E/8zsjoLnRGDSASF8MvgimzV41\nlDODEGmJdnpY4BEVzWiOWKJ/NJ7OFFEO8S3FWSl8JgnHUlPVsSdLNxrefIN1cJim\nnk2Cc+CcaTBnytbG94ogRlAu4Vb4Fhn5+pUJZH9QcFUMOW0MVG5gbqmE3XVsXZjW\n9rb0WfnTBOUhU2kgKXLtFBdVXkp32iiK/J1tg//uJgKi4CoRdgGX0o7BpE9mI5Bw\nAzlz/IZ580+i2rc6Ns6/ncHR/i67OQY9/3/C4VXB3QBfnZh4WNnyvIQiAHeF7299\nkcNR9sLW+OVMUjWeAcH2viFZ+8ooxtuFB8zNs35VjpDngm3vlDsdeQlt5WxGrfLT\nfqmhcANL8KPPNWuXVYDRZJSzEeE+hfG5IJWEeOGmHvPgLxoVpD6sYC0FSQEx/Dc\nL9Kfe9COaPR0Dov6m+qcXBixLW1Vja/wGYKd6NEiJEHYSPNF5jSxVE9tdXHxIb2Q\n6yZUtOuWTqD5uRWT4IX0W3jl2JwF1RAwroVDVGnoIUzTvB/fKj11SmVYOrFRumh7\nAY2WjD5WimbxJnVOSiWNr318vdCzAoFELBzUC6JNFm3Q5VTrET0toUEycivGGQLV\nps5NBvcffO0cqL3yO38UBBktW34IDnTdPcbXlDaD1HAApSG4fEziFfDb6YEkwZhe\n7KMHDgiUQFM1ao916Tcxtg+OsFCso6c6yu1h3y+NqiIxyLYU+nJUPqHJSLekEWCr\nOJC3LQXSZR9Lz6+HqpovO1/U/7JHRgM5UliyN63x6Ybozn5UFooP+m6ZniJ2qINk\nLQupUD/fzKGxivCtkwtqDNystXQadWJZQTW/ORECaVCBnVkRzHRc4t4nxE1k8akz\nwaqm3WLwVLSwgx0O/m2dtBk1gb7aOdbeYyMKSIK3pa52xx2qEazw5/3luwIPUb2W\nBmIHddPmFmKvzr3gVim4LcB+M4vbdaxSC+wB9nvQ8L5VgBz7BW8yoQwVvvhI1mZ6\n9msuQJCDX90lBy2bl1IwcwO9gR3IWjVl4rF7frnXiB/gK/yFWOs6RnGqFFCBrYSm\n-----END RSA PRIVATE KEY-----\n"

    encoded_jwt = jwt.encode(claims, secret, algorithm='HS256').decode('UTF-8') # RS256
    my_response = jsonify({'message': 'Authenticated'})
    my_response.headers['JWT'] = encoded_jwt
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
