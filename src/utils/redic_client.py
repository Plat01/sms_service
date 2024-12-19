import redis

from src.settings import settings

class RedisClient:
    EXPIRE_TIME = 5 * 60

    def __init__(self, host: str, port: int, db: int = 0, password: str = None):
        self.redis = redis.Redis(host=host, port=port, db=db, password=password)

    def set(self, key: str, value: str, expire: int = EXPIRE_TIME) -> bool:
        try:
            self.redis.set(key, value, ex=expire)
            return True
        except redis.exceptions.ConnectionError:
            return False
        

    def get(self, key: str) -> str:
        result = self.redis.get(key)
        return result.decode("utf-8") if result else None
    
    def delete(self, key: str) -> bool:
        try:
            self.redis.delete(key)
            return True
        except redis.exceptions.ConnectionError:
            return False
        

def get_redis_client():
    return RedisClient(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
