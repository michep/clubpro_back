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
# @jwt_required()
def createUser():
    return jsonify(DBUser.createUser(request.json))

@bp.route('/<userid>', methods=['PUT'])
@jwt_required()
def updateUser(userid: str):
    return jsonify(DBUser.updateUser(userid, request.json))

@bp.route('/register', methods=['PUT'])
# @jwt_required()
def registerUser():
    return jsonify(DBUser.registerUser(request.json))

@bp.route('/sendcode', methods=['PUT'])
# @jwt_required()
def sendCode():
    return jsonify(DBUser.sendSMS(request.json))


@bp.route('/checkcode', methods=['PUT'])
# @jwt_required()
def checkCode():
    return jsonify(DBUser.checkSMS(request.json))
