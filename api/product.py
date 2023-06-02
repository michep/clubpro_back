from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from services.dbproduct import DBProduct

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('', methods=['PUT'])
@jwt_required()
def createProduct():
    return jsonify(DBProduct.createProduct(request.json))


@bp.route('/<productid>', methods=['POST'])
@jwt_required()
def updateFolder(productid: str):
    return jsonify(DBProduct.updateProduct(productid, request.json))


@bp.route('/<productid>', methods=['GET'])
@jwt_required()
def getFolderById(productid: str):
    return jsonify(DBProduct.getProductById(productid))
