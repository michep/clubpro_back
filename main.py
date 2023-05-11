from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from datetime import timedelta
from jsonprovider import MongoJSONProvider

from auth import authenticate, identity, make_payload_handler, auth_response_handler
from config import SECRET_KEY

from api.user import bp as userbp

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=3)
app.json = MongoJSONProvider(app)

CORS(app)

jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)
jwt.jwt_payload_handler(make_payload_handler(app))
jwt.auth_response_handler(auth_response_handler)

app.register_blueprint(userbp)

app.run('0.0.0.0', port='8083')
