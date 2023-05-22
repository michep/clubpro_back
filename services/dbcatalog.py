from bson import ObjectId
from mdb import MDB


class DBCatalog:

    @classmethod
    def projection(self, allattrs: bool):
        if not allattrs:
            return {'password': 0}

    @classmethod
    def getFolderById(self, id: str | ObjectId) -> dict | None:
        if type(id) is str:
            id = ObjectId(id)
        return MDB.catalog.find_one({'_id': id})

    @classmethod
    def getSubFoldersByParentId(self, id: str | ObjectId | None) -> dict | None:
        if type(id) is str:
            id = ObjectId(id)
        return list(MDB.catalog.find({'parentfolder_id': id}))

    @classmethod
    def createFolder(self, data: dict) -> dict:
        return {'inserted_id': MDB.catalog.insert_one(data).inserted_id}

    @classmethod
    def updateFolder(self, id: str | ObjectId, setdata: dict, unsetdata: dict = {}) -> dict:
        if type(id) is str:
            id = ObjectId(id)
        res = MDB.catalog.update_one(
            {'_id': id}, {'$set': setdata, '$unset': unsetdata})
        return {'modified_count': res.modified_count, 'upserted_id': res.upserted_id}

    @classmethod
    def getFolderPrimaryProducts(self, id: str | ObjectId) -> dict | None:
        if type(id) is str:
            id = ObjectId(id)
        return list(MDB.product.find({'parentfolder_id': id}))

    @classmethod
    def getFolderSecondaryProducts(self, id: str | ObjectId) -> dict | None:
        if type(id) is str:
            id = ObjectId(id)
        return list(MDB.product.find({'secondaryfolder_ids': id}))
