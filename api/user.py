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
    return jsonify(DBUser.getUserByLogin(login, allattrs=True))


@bp.route('', methods=['PUT'])
@jwt_required()
def createUser():
    return jsonify(DBUser.createUser(request.json))


@bp.route('/<userid>', methods=['PUT'])
@jwt_required()
def updateUser(userid: str):
    return jsonify(DBUser.updateUser(userid, request.json))


@bp.route('/register', methods=['PUT'])
def registerUser():
    return jsonify(DBUser.registerUser(request.json))


@bp.route('/register/<userid>/sendcode', methods=['PUT'])
def sendCode(userid: str):
    return jsonify(DBUser.sendSMS(userid, request.json))


@bp.route('/register/<userid>/checkcode', methods=['PUT'])
def checkCode(userid: str):
    return jsonify(DBUser.checkSMS(userid, request.json))


@bp.route('/register/<userid>', methods=['PUT'])
def registerUser2(userid: str):
    return jsonify(DBUser.updateUser(userid, request.json))
