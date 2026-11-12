from redis.asyncio import Redis
from app.redis.base import redis_ping, redis_client
from app.redis.user import UserStore
from app.redis.activity import ActivityStore

class Store:
    def __init__(self, client: Redis = redis_client, **kwargs):
        self.client = client
        self.kwargs = kwargs

        self.user = UserStore(client, **kwargs)
        self.activity = ActivityStore(client, **kwargs)

    @classmethod
    async def ping(self):
        return await redis_ping(True)

    @classmethod
    async def close(self):
        return await redis_client.aclose()

store = Store()