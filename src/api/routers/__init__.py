from fastapi import APIRouter

from src.api.routers import auth, sms, telegram

api_router = APIRouter()

api_router.include_router(sms.router, prefix="/sms", tags=["sms"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(telegram.router, prefix="/telegram", tags=["telegram"])

