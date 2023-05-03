from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from datetime import timedelta
from jsonprovider import MongoJSONProvider

from auth import authenticate, identity, make_payload_handler

from api.user import bp as userbp

app = Flask(__name__)

app.config['SECRET_KEY'] = '971b8f53-f482-497b-8292-e8d6a5f9663d'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=3)
app.json = MongoJSONProvider(app)

CORS(app)

jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)
jwt.jwt_payload_handler(make_payload_handler(app))



app.register_blueprint(userbp)

app.run('0.0.0.0', port='8083')
