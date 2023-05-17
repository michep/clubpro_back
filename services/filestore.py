from bson import ObjectId
from mdb import MDB
import gridfs


class Filestore:

    @classmethod
    def uploadFile(self, data: bytes | str, filename: str):
        return {'fileid': gridfs.GridFS(MDB).put(data, filename=filename)}

    @classmethod
    def getFile(self, fileid: str | ObjectId):
        if type(fileid) is str:
            fileid = ObjectId(fileid)
        try:
            res = gridfs.GridFS(MDB).get(file_id=fileid)
        except:
            res = None
        return res

    @classmethod
    def deleteFile(self, fileid: str | ObjectId):
        if type(fileid) is str:
            fileid = ObjectId(fileid)
        return gridfs.GridFS(MDB).delete(file_id=fileid)
