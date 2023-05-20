from typing import Any
from dateutil import parser
from flask.json.provider import DefaultJSONProvider
from bson import ObjectId, tz_util
from datetime import datetime


class MongoJSONProvider(DefaultJSONProvider):
    def dumps(self, obj: Any, **kwargs: Any) -> str:
        if type(obj) is ObjectId:
            obj = self.__dumpObjectId(obj)

        elif type(obj) is datetime:
            obj = self.__dumpDatetime(obj)

        elif type(obj) is list:
            obj = self.__dumpList(obj)

        elif type(obj) is dict:
            obj = self.__dumpDict(obj)

        return super().dumps(obj, **kwargs)

    def loads(self, s: str | bytes, **kwargs: Any) -> Any:
        data = super().loads(s, **kwargs)

        if type(data) is dict:
            data = self.__loadDict(data)

        elif type(data) is list:
            data = self.__loadList(data)

        elif self.__isDatetime(data):
            data = self.__loadDatetime(data)

        elif self.__isObjectId(data):
            data = self.__loadObjectId(data)

        return data

    def __dumpObjectId(self, val: ObjectId) -> str:
        return str(val)

    def __dumpDatetime(self, val: datetime) -> str:
        if not val.tzinfo:
            val = val.replace(tzinfo=tz_util.utc)
            assert val.tzinfo is not None
        off = val.tzinfo.utcoffset(val)
        if (off.days, off.seconds, off.microseconds) == (0, 0, 0):  # type: ignore
            tz_string = "Z"
        else:
            tz_string = val.strftime("%z")
        millis = int(val.microsecond / 1000)
        fracsecs = ".%03d" % (millis,) if millis else ""
        return "%s%s%s" % (val.strftime("%Y-%m-%dT%H:%M:%S"), fracsecs, tz_string)

    def __dumpList(self, val: list) -> list:
        for i in range(len(val)):
            data = val[i]

            if type(data) is ObjectId:
                val[i] = self.__dumpObjectId(data)
                continue

            if type(data) is datetime:
                val[i] = self.__dumpDatetime(data)
                continue

            if type(data) is list:
                val[i] = self.__dumpList(data)
                continue

            if type(data) is dict:
                val[i] = self.__dumpDict(data)

        return val

    def __dumpDict(self, val: dict) -> dict:
        for key in val.keys():
            data = val[key]

            if type(data) is ObjectId:
                val[key] = self.__dumpObjectId(data)
                continue

            if type(data) is datetime:
                val[key] = self.__dumpDatetime(data)

            if type(data) is list:
                val[key] = self.__dumpList(data)
                continue

            if type(data) is dict:
                val[key] = self.__dumpDict(data)

        return val


    def __loadObjectId(self, val: str) -> ObjectId:
        return ObjectId(val)


    def __loadDatetime(self, val: str) -> datetime:
        return parser.parse(val)


    def __loadList(self, val: list) -> list:
        for i in range(len(val)):
            data = val[i]

            if type(data) is dict:
                val[i] = self.__loadDict(data)

            elif type(data) is list:
                val[i] = self.__loadList(data)

            elif self.__isDatetime(data):
                val[i] = self.__loadDatetime(data)

            elif self.__isObjectId(data):
                val[i] = self.__loadObjectId(data)

        return val


    def __loadDict(self, val: dict) -> dict:
        for key in val.keys():
            data = val[key]
        
            if type(data) is dict:
                val[key] = self.__loadDict(data)

            elif type(data) is list:
                val[key] = self.__loadList(data)

            elif self.__isDatetime(data):
                val[key] = self.__loadDatetime(data)

            elif self.__isObjectId(data):
                val[key] = self.__loadObjectId(data)

        return val


    def __isObjectId(self, val: str) -> bool:
        return type(val) is str and self.__isHex(val) and len(val) == 24


    def __isDatetime(self, val: str) -> bool:
        return type(val) is str and len(val) > 15 and val[4] == '-' and val[7] == '-' and val[13] == ':'


    def __isHex(self, s):
        try:
            int(s, 16)
        except ValueError:
            return False
        return len(s) % 2 == 0
