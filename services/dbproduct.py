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


    @classmethod
    def createProduct(self, data: dict) -> dict:
        return {'inserted_id': MDB.product.insert_one(data).inserted_id}

    @classmethod
    def updateProduct(self, id: str | ObjectId, setdata: dict, unsetdata: dict = {}) -> dict:
        if type(id) is str:
            id = ObjectId(id)
        res = MDB.product.update_one(
            {'_id': id}, {'$set': setdata, '$unset': unsetdata})
        return {'modified_count': res.modified_count, 'upserted_id': res.upserted_id}
