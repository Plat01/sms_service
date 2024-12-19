from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas.sms import PhoneNumberInput
from src.api.schemas.telegram import TelegramErrors, TelegramResponse
from src.hadlers.send_code import CodeMaker
from src.utils.redic_client import RedisClient, get_redis_client
from src.utils.send_tg_code import TelegramSender


router = APIRouter()

@router.post('/send-code', response_model=TelegramResponse)
async def send_tg_code(data: PhoneNumberInput, redis: RedisClient = Depends(get_redis_client)):
    code = CodeMaker._make_code()
    if not redis.set(data.phone_number, code):
        raise HTTPException(
            status_code=500,
            detail="Can't save code to redis"
        ) 
    responce = await TelegramSender.send_code(data.phone_number, code=code)
    if responce.error == TelegramErrors.PHONE_NUMBER_INVALID.value:
            raise HTTPException(status_code=400, detail="Phone number is invalid")
    return responce