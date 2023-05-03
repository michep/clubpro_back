from typing import Any
from dateutil import parser
from flask.json.provider import DefaultJSONProvider
from bson import ObjectId, tz_util
from datetime import datetime

class MongoJSONProvider(DefaultJSONProvider):
    def dumps(self, obj: Any, **kwargs: Any) -> str:
        if type(obj) is dict:
            for key in obj.keys():
                val = obj[key]

                if type(val) is ObjectId:
                    obj[key] = str(val)

                elif type(val) is datetime:
                    if not val.tzinfo:
                        val = val.replace(tzinfo=tz_util.utc)
                        assert val.tzinfo is not None
                    off = val.tzinfo.utcoffset(val)
                    if (off.days, off.seconds, off.microseconds) == (0, 0, 0):  # type: ignore
                        tz_string = "Z"
                    else:
                        tz_string = obj.strftime("%z")
                    millis = int(obj.microsecond / 1000)
                    fracsecs = ".%03d" % (millis,) if millis else ""
                    obj[key] = "%s%s%s" % (obj.strftime("%Y-%m-%dT%H:%M:%S"), fracsecs, tz_string)

        return super().dumps(obj, **kwargs)


    def loads(self, s: str | bytes, **kwargs: Any) -> Any:
        data = super().loads(s, **kwargs)
        if type(data) is dict:
            for key in data.keys():
                if type(data[key]) is str and len(data[key]) == 24 and key.endswith('_id'):
                    data[key] = ObjectId(data[key])
                    continue
                if type(data[key]) is list and key.endswith('_ids'):
                    for i in range(len(data[key])):
                        if type(data[key][i]) is str and len(data[key][i]) == 24:
                            data[key][i] = ObjectId(data[key][i])
                    continue
                if type(data[key]) is str and len(data[key]) > 15 and data[key][4] == '-' and data[key][7] == '-' and data[key][13] == ':':
                    data[key] = parser.parse(data[key])
        elif type(data) is list:
            for i in range(len(data)):
                if type(data[i]) is str and len(data[i]) == 24:
                    data[i] = ObjectId(data[i])
        return data
