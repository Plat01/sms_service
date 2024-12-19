from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routers import api_router
from src.settings import settings

# async def lifespan(app: FastAPI):
#     # TODO: delete old records
#     pass

app = FastAPI(
    root_path=settings.API_V1_STR,
    title="SMSService API",
    version="0.1.0",
    docs_url=f"/docs",
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "localhost:3000",
        "0.0.0.0:3000",
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        'https://vsegda-daem.ru/',
        'http://vsegda-daem.ru/',
    ],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(api_router)
