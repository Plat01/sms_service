from typing import Any, List, Optional
from pydantic import BaseModel, Field

class PhoneNumberInput(BaseModel):
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$') 

    class Config:
        schema_extra = {
            "example": {
                "phone_number": "+1234567890"
            }
        }

class CodeAndPhone(BaseModel):
    phone_number: str
    code: str

    class Config:
        schema_extra = {
            "example": {
                "phone_number": "+1234567890",
                "random_code": "1234"
            }
        }


class SMSDataItem(BaseModel):
    message: str
    createdAt: int
    id: int
    tag: str | None
    status: str
    phone: str

class DoublesError(BaseModel):
    errorDescription: str
    errorCode :str
    tag: str | None
    status: str = "Error"
    phone: str

class SMSResponse(BaseModel):
    source: str = "SMS"
    status: str
    data: SMSDataItem | DoublesError

