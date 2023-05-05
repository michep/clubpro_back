from bson import ObjectId
from mdb import MDB
from services.utils import generatecode3

class DBUser:

    @classmethod
    def projection(self, allattrs: bool):
        if not allattrs:
            return {'password': 0}

    @classmethod
    def getOneUserByFilter(self, filter: dict, allattrs: bool = False) -> dict|None:
        return MDB.user.find_one(filter, DBUser.projection(allattrs))

    @classmethod
    def getManyUsersByFilter(self, filter: dict, allattrs: bool = False) -> dict|None:
        return MDB.user.find(filter, DBUser.projection(allattrs))

    @classmethod
    def getUserById(self, userid: str|ObjectId, allattrs: bool = False) -> dict|None:
        if type(userid) is str:
            userid = ObjectId(userid)
        return MDB.user.find_one({'_id': userid}, DBUser.projection(allattrs))

    @classmethod
    def getUserByLogin(self, login: str, allattrs: bool = False) -> dict|None:
        return MDB.user.find_one({'login': login}, DBUser.projection(allattrs))

    @classmethod
    def createUser(self, data: dict) -> dict:
        return {'inserted_id': MDB.user.insert_one(data).inserted_id}

    @classmethod
    def updateUser(self, userid: str|ObjectId, setdata: dict, unsetdata: dict = {}) -> dict:
        if type(userid) is str:
            userid = ObjectId(userid)
        return {'modified_count': MDB.user.update_one({'_id': userid}, {'$set': setdata, '$unset': unsetdata}).modified_count}
    
    @classmethod
    def sendSMS(self, userid: str|ObjectId, data: dict) -> dict:
        if type(userid) is str:
            userid = ObjectId(userid)
        code = generatecode3()
        # code = '0000'
        DBUser.updateUser(userid, {'smscode': code}, {'phone_confirmed': 1})
        return {'result': 'sent'}

    @classmethod
    def checkSMS(self, userid: str|ObjectId, data: dict) -> dict:
        if type(userid) is str:
            userid = ObjectId(userid)
        user = DBUser.getUserById(userid)
        if 'smscode' in user.keys() and 'smscode' in data.keys() and user['smscode'] == data['smscode']:
            DBUser.updateUser(user['_id'], {'phone_confirmed': True}, {'smscode': 1})
            return {'result': 'ok'}
        else:
            return {'result': 'error'}

    @classmethod
    def registerUser(self, data: dict) -> dict:
        user = DBUser.getUserByLogin(data['login'])
        if user:
            return {'inserted_id': None, 'error': 'такой номер телефона уже использован'}

        return DBUser.createUser(data)
