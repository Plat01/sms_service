import aiohttp
from aiohttp.client_exceptions import ClientConnectorDNSError

from src.api.schemas.sms import SMSResponse
from src.settings import settings


class SMSSender:

    API_KEY = settings.SMS_KEY
    URL = settings.SMS_SEND_URL
    HEADERS = {
        'Content-Type': 'application/json',
    }

    @classmethod
    async def send_sms(cls, phone, text, plane_at: int = None):
        sms = {
            "channel": "char",
            "sender": "Banki.Promo",
            "text": text,
            "phone": phone,
        }
        if plane_at:
            sms["plannedAt"] = plane_at
        payload = {
            "apiKey": cls.API_KEY,
            "sms": [sms],
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(cls.URL, json=payload, headers=cls.HEADERS) as response:
                    response = await response.json()
                    return SMSResponse(
                        status=response.get('status'),
                        data=response.get('data')[0]
                    )
        except ClientConnectorDNSError as e:
            raise ConnectionError(str(e))
