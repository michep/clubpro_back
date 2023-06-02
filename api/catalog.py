from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from services.dbcatalog import DBCatalog

bp = Blueprint('catalog', __name__, url_prefix='/catalog')


@bp.route('/<folderid>', methods=['GET'])
@jwt_required()
def getFolderById(folderid: str):
    return jsonify(DBCatalog.getFolderById(folderid))


@bp.route('/root', methods=['GET'])
@jwt_required()
def getRootFolders():
    return jsonify(DBCatalog.getSubFoldersByParentId(None))


@bp.route('/<folderid>/subfolders', methods=['GET'])
@jwt_required()
def getSubFolders(folderid: str):
    return jsonify(DBCatalog.getSubFoldersByParentId(folderid))


@bp.route('/<folderid>/products/<type>', methods=['GET'])
@jwt_required()
def getProductsOfType(folderid: str, type: str):
    res = []
    if type == 'all':
        res.extend(DBCatalog.getFolderPrimaryProducts(folderid))
        res.extend(DBCatalog.getFolderSecondaryProducts(folderid))
    elif type == 'primary':
        res.extend(DBCatalog.getFolderPrimaryProducts(folderid))
    elif type == 'secondary':
        res.extend(DBCatalog.getFolderSecondaryProducts(folderid))
    return jsonify(res)


@bp.route('', methods=['PUT'])
@jwt_required()
def createFolder():
    return jsonify(DBCatalog.createFolder(request.json))


@bp.route('/<folderid>', methods=['POST'])
@jwt_required()
def updateFolder(folderid: str):
    return jsonify(DBCatalog.updateFolder(folderid, request.json))
