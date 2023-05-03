from pymongo.results import InsertOneResult
from bson import ObjectId
from mdb import MDB


class DBUser:
    @classmethod
    def projection(self, allattrs: bool):
        if not allattrs:
            return {'password': 0}

    @classmethod
    def getUserById(self, id: str, allattrs: bool = False) -> dict|None:
        return MDB.user.find_one({'_id': ObjectId(id)}, DBUser.projection(allattrs))

    @classmethod
    def getUserByLogin(self, login: str) -> dict|None:
        return MDB.user.find_one({'login': login})


    @classmethod
    def createUser(self, data: dict) -> dict|None:
        return {'inserted_id': MDB.user.insert_one(data).inserted_id}
