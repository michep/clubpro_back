from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from services.dbuser import DBUser

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<userid>', methods=['GET'])
@jwt_required()
def getUser(userid: str):
    return jsonify(DBUser.getUserById(userid))

@bp.route('', methods=['PUT'])
@jwt_required()
def createUser():
    data = request.json
    return jsonify(DBUser.createUser(data))