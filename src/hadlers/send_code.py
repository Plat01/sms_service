
import random

from fastapi import HTTPException

from src.api.schemas.telegram import TelegramErrors, TelegramResponse
from src.utils.redic_client import RedisClient
from src.utils.send_tg_code import TelegramSender
from src.utils.sms_semder import SMSSender


class CodeMaker:
    @classmethod
    def make_code(cls, length: int = 4) -> str:
        return str(random.randint(1, 9999)).zfill(length)

    
class CodeSender:
    
    @classmethod
    async def send_code(cls, db: RedisClient, phone: str):
        code: str = CodeMaker.make_code()
        if not db.set(phone, code):
             raise Exception("Can't save code to redis")  # TODO: delete Exeption
        response = await TelegramSender.send_code(phone, code)
        if response.ok:
            return response
        if response.error == TelegramErrors.PHONE_NUMBER_INVALID.value:
            raise HTTPException(status_code=400, detail="Phone number is invalid")
        
        responce = await SMSSender.send_sms(phone=phone, 
                                            text=f"Код: {code}\nvsegda-daem.ru")
        return responce


    