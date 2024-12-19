from datetime import datetime, timedelta, timezone
import jwt

from src.api.schemas.jwt_shemas import JWTExp, TockenPayload, TokenErrorResponse
from src.settings import settings


class JWTManager:

    SECRET_KEY: str = settings.JWT_KEY
    ALGORITHM: str = settings.JWT_ALGORITHM
    EXPIRES_DELTA: timedelta = timedelta(days=30)
        
    @classmethod
    def create_access_token(cls, 
                            user_phone: str, 
                            expires_delta: timedelta | None = None
                            ) -> JWTExp:
        expire = datetime.now(tz=timezone.utc) + \
            (expires_delta if expires_delta else cls.EXPIRES_DELTA)
        
        expire_timestamp = int(expire.timestamp())

        to_encode = {
            "exp": expire_timestamp,
            "phone_number": user_phone
        }

        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

        return JWTExp(exp=expire_timestamp, jwt=encoded_jwt)
    
    @classmethod
    def decode_token(cls, token: str) -> TockenPayload | TokenErrorResponse:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return TockenPayload(**payload)
        except jwt.ExpiredSignatureError as e:
            payload = {
                "error": "Token has expired",
                "error_message": str(e)
            }
            return TokenErrorResponse(**payload)
        except jwt.InvalidTokenError as e:
            payload = {
                "error": "Token is invalid",
                "error_message": str(e)
            }
            return TokenErrorResponse(**payload)
    