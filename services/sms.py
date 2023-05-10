import requests
from config import SMS_RU_API_KEY

class SMS:
    @classmethod
    def sendSMS(self, phone: str, message: str):
        response = requests.post(
            "https://sms.ru/sms/send",
            params={
                'api_id': SMS_RU_API_KEY,
                'to': phone,
                'msg': message,
                'json': 1
            },
        )
        return response.json()
