from flask import Blueprint, jsonify, request, send_file, Response
from flask_jwt import jwt_required
import base64
from services.filestore import Filestore

bp = Blueprint('file', __name__, url_prefix='/file')


@bp.route('', methods=['PUT'])
@jwt_required()
def uploadFile():
    data = base64.b64decode(request.json['data'])
    return jsonify(Filestore.uploadFile(data=data, filename=request.json['filename'], fileid=request.json['_id']))


@bp.route('/<fileid>', methods=['GET'])
@jwt_required()
def getFile(fileid: str):
    gridout = Filestore.getFile(fileid=fileid)
    if gridout == None:
        return Response(status=204)
    return send_file(gridout, download_name=gridout.filename)


@bp.route('/<fileid>', methods=['DELETE'])
@jwt_required()
def deleteFile(fileid: str):
    return jsonify(Filestore.deleteFile(fileid=fileid))


@bp.route('/delete', methods=['POST'])
@jwt_required()
def uploadFiles():
    return jsonify(Filestore.deleteFiles(request.json))
