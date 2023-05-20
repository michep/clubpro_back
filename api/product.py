from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from services.dbproduct import DBProduct

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/<productid>', methods=['GET'])
@jwt_required()
def getFolderById(productid: str):
    return jsonify(DBProduct.getProductById(productid))
