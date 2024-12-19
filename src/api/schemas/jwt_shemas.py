from pydantic import BaseModel


class JWT(BaseModel):
    token: str

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
            }
        }

class JWTExp(BaseModel):
    exp: int
    jwt: str

class PhoneAndJWT(BaseModel):
    phone_number: str
    jwt: str


class TockenPayload(BaseModel):
    phone_number: str
    exp: int

class TokenErrorResponse(BaseModel):
    error: str
    error_message: str
