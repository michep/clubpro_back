from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.results import InsertOneResult
from bson import ObjectId
from config import MONGODB_CONNECTION

MDB: Database = MongoClient(MONGODB_CONNECTION).get_database('clubpro')

class MDBClient:

    class User:
        @classmethod
        def projection(self, allattrs: bool):
            if not allattrs:
                return {'password': 0}

        @classmethod
        def getUserById(self, id: str, allattrs: bool = False) -> dict|None:
            return MDB.user.find_one({'_id': ObjectId(id)}, MDBClient.User.projection(allattrs))

        @classmethod
        def getUserByLogin(self, login: str) -> dict|None:
            return MDB.user.find_one({'login': login})


        @classmethod
        def createUser(self, data: dict) -> dict|None:
            return MDB.user.insert_one(data)
