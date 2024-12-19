from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.jwt_shemas import JWT, PhoneAndJWT, TokenErrorResponse
from src.database import get_session
from src.repository.user import UserCrud
from src.utils.jwt_manager import JWTManager


router = APIRouter()

@router.post('/validate-jwt', response_model=PhoneAndJWT, status_code=200)
async def validate_jwt(
    data: PhoneAndJWT,
    session: AsyncSession = Depends(get_session)
):
    
    decoded_token = JWTManager.decode_token(data.token)

    if isinstance(decoded_token, TokenErrorResponse):
        raise HTTPException(status_code=403, detail=decoded_token.model_dump())
    
    user_data = await UserCrud.get_by_phone_number(
        session=session,
        phone_number=decoded_token.phone_number
        )
    
    if not user_data:
        raise HTTPException(status_code=403, detail="User with this token not found")
    
    if user_data.expiration_time < datetime.now(tz=timezone.utc).timestamp():
        raise HTTPException(status_code=403, detail="Token has expired")
    
    if user_data.phone_number != data.phone_number:
        raise HTTPException(status_code=403, detail="Wrong phone number")
    
    return PhoneAndJWT(
        phone_number=decoded_token.phone_number,
        jwt=data.token
    )

@router.post('/refresh-jwt', status_code=200)
async def refresh_jwt(
    data: PhoneAndJWT,
    session: AsyncSession = Depends(get_session)
):
    
    pass


@router.head('/validate-jwt', status_code=200)
async def validate_jwt(
    session: AsyncSession = Depends(get_session)
):
    pass


# @router.post('/validate-token', response_model=PhoneAndJWT, status_code=200)
# async def validate_token(
#     data: JWT,
#     session: AsyncSession = Depends(get_session)
# ):
#     decoded_token = JWTManager.decode_token(data.token)

#     if isinstance(decoded_token, TokenErrorResponse):
#         raise HTTPException(status_code=403, detail=decoded_token.model_dump())
    
#     user_data = await UserCrud.get_by_phone_number(
#         session=session,
#         phone_number=decoded_token.phone_number
#         )
    
#     if not user_data:
#         raise HTTPException(status_code=403, detail="User with this token not found")
    
#     if user_data.expiration_time < datetime.now(tz=timezone.utc).timestamp():
#         raise HTTPException(status_code=403, detail="Token has expired")
    
#     return PhoneAndJWT(
#         phone_number=decoded_token.phone_number,
#         jwt=data.token
#     )
