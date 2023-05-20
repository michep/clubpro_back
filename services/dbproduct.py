from bson import ObjectId
from mdb import MDB

class DBProduct:

    @classmethod
    def projection(self, allattrs: bool):
        if not allattrs:
            return {'password': 0}


    @classmethod
    def getProductById(self, id: str|ObjectId) -> dict|None:
        if type(id) is str:
            id = ObjectId(id)
        return MDB.product.find_one({'_id': id})
