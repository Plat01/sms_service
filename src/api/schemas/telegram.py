from enum import Enum
from pydantic import BaseModel


class DeliveryStatus(BaseModel):
    status: str
    updated_at: int

class Result(BaseModel):
    request_id: str
    phone_number: str
    request_cost: float
    remaining_balance: float
    delivery_status: DeliveryStatus

class SuccessResponse(BaseModel):
    ok: bool
    result: Result

class ErrorResponse(BaseModel):
    ok: bool
    error: str

class TelegramResponse(BaseModel):
    source: str = "Telegram"
    ok: bool
    result: None | Result = None
    error: None| str = None

class TelegramErrors(Enum):
    PHONE_NUMBER_INVALID:  str = "PHONE_NUMBER_INVALID"
    PHONE_NUMBER_NOT_FOUND: str = "PHONE_NUMBER_NOT_FOUND"
    PHONE_NUMBER_NOT_VERIFIED: str = "PHONE_NUMBER_NOT_VERIFIED"