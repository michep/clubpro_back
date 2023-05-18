from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from services.dbuser import DBUser

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<userid>', methods=['GET'])
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


@bp.route('/<userid>', methods=['POST'])
@jwt_required()
def updateUser(userid: str):
    return jsonify(DBUser.updateUser(userid, request.json))


@bp.route('/register', methods=['PUT'])
def registerUser():
    return jsonify(DBUser.registerUser(request.json))


@bp.route('/register/<userid>', methods=['PUT'])
def registerUser2(userid: str):
    return jsonify(DBUser.updateUser(userid, request.json))


@bp.route('/sendcode', methods=['POST'])
def sendCode():
    return jsonify(DBUser.sendSMS(request.json))


@bp.route('/checkcode', methods=['POST'])
def checkCode():
    return jsonify(DBUser.checkSMS(request.json))


@bp.route('/resetpassword', methods=['PUT'])
def resetpassword():
    return jsonify(DBUser.resetpassword(request.json))
