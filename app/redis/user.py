from app.redis.base import BaseStore, BaseHashs

class UserHashs(BaseHashs):
    TG_HASH = "telegram_id"
    GENERAL_HASH = "general_id"

class UserStore(BaseStore):
    hashs_cls = UserHashs
    hashs: type[UserHashs]
    
    async def get_user_id(self, tg_id: int) -> int | None:
        v = await self.client.hget(self.hashs_cls.TG_HASH, tg_id)
        return int(v) if v else None
    
    async def get_tg_id(self, user_id: int) -> int | None:
        v = await self.client.hget(self.hashs_cls.GENERAL_HASH, user_id)
        return int(v) if v else None

    async def hscan_all(self, key: str, batch: int = 1000):
        cursor = 0
        cursor, chunk = await self.client.hscan(key, cursor=cursor, count=batch)
        return chunk
