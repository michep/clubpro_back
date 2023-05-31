from bson import ObjectId
from mdb import MDB
from services.utils import generatecode3
from services.sms import SMS

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
        return list(MDB.user.find(filter, DBUser.projection(allattrs)))


    @classmethod
    def getUserById(self, id: str|ObjectId, allattrs: bool = False) -> dict|None:
        if type(id) is str:
            id = ObjectId(id)
        return MDB.user.find_one({'_id': id}, DBUser.projection(allattrs))


    @classmethod
    def getUserByLogin(self, login: str, allattrs: bool = False) -> dict|None:
        return MDB.user.find_one({'login': login}, DBUser.projection(allattrs))


    @classmethod
    def createUser(self, data: dict) -> dict:
        return {'inserted_id': MDB.user.insert_one(data).inserted_id}


    @classmethod
    def updateUser(self, id: str|ObjectId, setdata: dict, unsetdata: dict = {}) -> dict:
        if type(id) is str:
            id = ObjectId(id)
        res = MDB.user.update_one({'_id': id}, {'$set': setdata, '$unset': unsetdata})
        return {'modified_count': res.modified_count, 'upserted_id': res.upserted_id}
    

    @classmethod
    def sendSMS(self, data: dict) -> dict:
        user = DBUser.getUserByLogin(data['login'])
        if not user:
            return {'result': 'error'}
        code = generatecode3()
        # code = '0000'
        DBUser.updateUser(user['_id'], {'smscode': code}, {'phone_confirmed': 1})
        # smsres = SMS.sendSMS(data['login'], f'ClubPRO ваш код подтверждения {code}')
        smsres = {'status': 'OK'}
        if smsres['status'] == 'ERROR':
            return {'result': 'error'}

        return {'result': 'sent'}


    @classmethod
    def checkSMS(self, data: dict) -> dict:
        user = DBUser.getUserByLogin(data['login'])
        if not user:
            return {'result': 'error'}
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


    @classmethod
    def resetpassword(self, data: dict) -> dict:
        smsres = DBUser.checkSMS(data)
        if smsres['result'] == 'ok':
            user = DBUser.getUserByLogin(data['login'])
            return DBUser.updateUser(user['_id'], {'login': data['login'], 'password': data['password']})
        return smsres
