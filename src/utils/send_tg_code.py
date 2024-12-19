import aiohttp

from src.api.schemas.telegram import TelegramResponse
from src.settings import settings


class TelegramSender:

    BASE_URL = 'https://gatewayapi.telegram.org/'
    TOKEN = settings.TG_TOKEN
    HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    @classmethod
    async def send_code(cls, phone: str, code: str):
        """_summary_

        Method sends code to TG user and return 

        {
        "ok": true,
        "result": {
            "request_id": "141665098367493",
            "phone_number": "79199173395",
            "request_cost": 0.01,
            "remaining_balance": 99.98,
            "delivery_status": {
                "status": "sent",
                "updated_at": 1730472088
                }
            }
        }

        {
        "ok": false,
        "error": "PHONE_NUMBER_INVALID"
        }

        Args:
            phone (str): phone in E.164 format
            code (str): 4 digit code

        Returns:
            _type_: _description_
        """

        json_body = {
            'phone_number': phone,
            'code_length': 4,
            'ttl': 120,
            'code': code
        }

        endpoint = 'sendVerificationMessage'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(cls.BASE_URL + endpoint, headers=cls.HEADERS, json=json_body) as response:
                    response = await response.json()
                    return TelegramResponse(**response)
        except aiohttp.ClientConnectorDNSError as e:
            TelegramResponse(ok=False, error=str(e))

            