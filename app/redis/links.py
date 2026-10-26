from app.redis.base import redis_client

class LinkHashs:
    TG_HASH = "telegram_id"
    GENERAL_HASH = "general_id"

class RedisLinks:
    client = redis_client
    links = LinkHashs

    async def get_user_id(self, tg_id: int) -> int | None:
        v = await self.client.hget(self.links.TG_HASH, tg_id)
        return int(v) if v else None
    
    async def get_tg_id(self, user_id: int) -> int | None:
        v = await self.client.hget(self.links.GENERAL_HASH, user_id)
        return int(v) if v else None

    async def hscan_all(self, key: str, batch: int = 1000):
        cursor = 0
        cursor, chunk = await self.client.hscan(key, cursor=cursor, count=batch)
        return chunk

links = RedisLinks()
