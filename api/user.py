from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from services.dbuser import DBUser

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/id/<userid>', methods=['GET'])
@jwt_required()
def getUserById(userid: str):
    return jsonify(DBUser.getUserById(userid))

@bp.route('/login/<login>', methods=['GET'])
@jwt_required()
def getUserByLogin(login: str):
    return jsonify(DBUser.getUserByLogin(login))

@bp.route('', methods=['PUT'])
@jwt_required()
def createUser():
    data = request.json
    return jsonify(DBUser.createUser(data))
