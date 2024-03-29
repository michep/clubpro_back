import datetime
from hmac import compare_digest
from services.dbuser import DBUser
from flask import jsonify


def authenticate(username, password):
    user = DBUser.getUserByLogin(username, allattrs=True)
    if user and compare_digest(user['password'].encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    return DBUser.getUserById(payload['identity'])


def make_payload_handler(current_app):

    def payload(payload):
        iat = datetime.datetime.utcnow()
        exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
        identity = str(payload['_id'])
        return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}
    
    return payload

def auth_response_handler(access_token, identity):
    try:
        token = access_token.decode('utf-8')
    except AttributeError:
        token = access_token
    return jsonify({'access_token': token})
