from config import settings
import redis.asyncio as redis

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True
)

async def redis_ping():
    return await redis_client.ping()
