import json
import random
from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.sms import PhoneNumberInput, CodeAndPhone, SMSResponse
from src.api.schemas.jwt_shemas import PhoneAndJWT
from src.api.schemas.telegram import TelegramResponse
from src.hadlers.send_code import CodeSender
from src.models.users import AuthUser
from src.repository.user import UserCrud
from src.utils.jwt_manager import JWTManager
from src.utils.redic_client import RedisClient, get_redis_client
from src.utils.sms_semder import SMSSender
from src.database import get_session


router = APIRouter()


# @router.post("/send-sms", response_model=SuccessResponse)
@router.post("/send-sms", response_model=Union[SMSResponse, TelegramResponse]) # TODO: add response_model
async def send_code(data: PhoneNumberInput, 
                   redis: RedisClient = Depends(get_redis_client),
                   session: AsyncSession = Depends(get_session)):
    """Route return SMSResponse, TelegramResponse models

    Args:
        data (PhoneNumberInput): just phone number
        redis (RedisClient, optional): Defaults to Depends(get_redis_client).

    Returns:
        _type_: _description_Z 
    """
    response = await CodeSender.send_code(redis, data.phone_number)
    
    return response


@router.post("/store-code", response_model=CodeAndPhone)
async def test_store_code(data: PhoneNumberInput, 
                        redis: RedisClient = Depends(get_redis_client)):
    
    random_code = str(random.randint(1, 9999)).zfill(4)
    
    if not redis.set(data.phone_number, random_code):
        raise HTTPException(status_code=500, detail="Can't save code to redis")
    
    return CodeAndPhone(
            phone_number=data.phone_number,
            code=random_code
        )


@router.post("/validate_sms_code", response_model=PhoneAndJWT)
async def validate_code(data: CodeAndPhone,
                        session: AsyncSession = Depends(get_session),
                        redis: RedisClient = Depends(get_redis_client)):
    code = redis.get(data.phone_number)
    
    if not code or code != data.code:
        raise HTTPException(status_code=400, detail="Invalid code or phone number")
    
    jwt = JWTManager.create_access_token(user_phone=data.phone_number)
    await UserCrud.create_or_update_record(
            session=session,
            phone_number=data.phone_number,
            jwt_token=jwt.jwt,
            expiration_time=jwt.exp
        )

    redis.delete(data.phone_number)
    
    return PhoneAndJWT(
            phone_number=data.phone_number,
            jwt=jwt.jwt
        )
