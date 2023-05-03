import datetime
from services.mongo import MDBClient


from hmac import compare_digest

# class User(object):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def __str__(self):
#         return "User(id='%s')" % self.id

# users = [
#     User(1, 'user1', 'abcxyz'),
#     User(2, 'user2', 'abcxyz'),
# ]

# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = MDBClient.User.getUserByLogin(username)
    if user and compare_digest(user['password'].encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    return MDBClient.User.getUserById(payload['identity'])


def make_payload_handler(current_app):

    def payload(payload):
        iat = datetime.datetime.utcnow()
        exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
        identity = str(payload['_id'])
        return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}
    
    return payload
