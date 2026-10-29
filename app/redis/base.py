from config import settings
import redis.asyncio as redis
from datetime import datetime
from app.logging.base import botlog
from app.exception.base import RedisError

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True
)

async def redis_ping(logged: bool = False):
            try:
                start = datetime.now()
                response = await redis_client.ping()
                if response:
                    end = datetime.now()
                    result = f'{int((end - start).total_seconds()*1000)}'
                    if logged:
                        botlog.logger.info('Redis работает', ping=result)
                    return result
                raise RedisError()
            except Exception as e:
                raise RedisError(error=str(e))