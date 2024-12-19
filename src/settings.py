from pydantic_settings import BaseSettings

class Settings(BaseSettings):


    API_V1_STR: str = "/sms/api"
    
    SMS_KEY: str
    SMS_SEND_URL: str = 'https://admin.p1sms.ru/apiSms/create'

    TG_TOKEN: str

    JWT_KEY: str
    JWT_ALGORITHM: str = "HS256"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "sms"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_CONNECTOR: str = "postgresql+asyncpg"

    @property
    def POSTGRES_URL(self):
        return f"{self.POSTGRES_CONNECTOR}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
