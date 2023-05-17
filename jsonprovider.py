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
            for i in range(len(obj)):
                val = obj[i]
                if self.__isObjectId(val=val):
                    obj[i] = self.__loadObjectId(val)

        elif type(obj) is dict:
            for key in obj.keys():
                val = obj[key]

                if type(val) is ObjectId:
                    obj[key] = self.__dumpObjectId(val)
                    continue

                if type(val) is datetime:
                    obj[key] = self.__dumpDatetime(val)

        return super().dumps(obj, **kwargs)
    

    def loads(self, s: str | bytes, **kwargs: Any) -> Any:
        data = super().loads(s, **kwargs)

        if type(data) is dict:
            for key in data.keys():
                val = data[key]
                if self.__isObjectId(val=val, key=key):
                    data[key] = self.__loadObjectId(val)
                    continue

                if self.__isObjectIdList(val=val, key=key):
                    for i in range(len(val)):
                        vali = data[key][i]
                        if self.__isObjectId(val=vali):
                            data[key][i] = self.__loadObjectId(vali)
                    continue

                if self.__isDatetime(val=val):
                    data[key] = self.__loadDatetime(val)

        elif type(data) is list:
            for i in range(len(data)):
                val = data[i]
                if self.__isObjectId(val=val):
                    data[i] = self.__loadObjectId(val)

        elif self.__isDatetime(val=data):
            data = self.__loadDatetime(val=data)

        elif self.__isObjectId(val=data):
            data = self.__loadObjectId(val=data)

        return data


    def __dumpObjectId(self, val: ObjectId, **kwargs: Any) -> str:
        return str(val)


    def __dumpDatetime(self, val: datetime, **kwargs: Any) -> str:
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


    def __isObjectId(self, val: str, key: str|None = None) -> bool:
        return type(val) is str and len(val) == 24 and (key == None or key.endswith('_id'))


    def __isObjectIdList(self, val: str, key: str|None = None) -> bool:
        return type(val) is list and (key == None or key.endswith('_ids'))
    

    def __isDatetime(self, val: str, key: str|None = None) -> bool:
        return type(val) is str and len(val) > 15 and val[4] == '-' and val[7] == '-' and val[13] == ':'


    def __loadObjectId(self, val: str) -> ObjectId:
        return ObjectId(val)
    

    def __loadDatetime(self, val: str) -> datetime:
        return parser.parse(val)
