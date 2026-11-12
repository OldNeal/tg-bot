import hashlib, json, unicodedata
from app.redis.base import BaseStore, BaseHashs
from app.exception.activity import (
    ActivityCooldownError,
    ActivityDuplicateError,
    ActivityLowDiversityError,
    ActivityMessageTooShortError,
    ActivityMessagePerRequestError
)

class ActivityHashs(BaseHashs):
    COOLDOWN = 'act:cd:{tg_id}'
    NGRAM_HISTORY = 'act:hist:{tg_id}'
    MESSAGE_COUNT = 'act:count:{tg_id}'

    @classmethod
    def cooldown(self, tg_id: int):
        return self.COOLDOWN.format(tg_id=tg_id)
    
    @classmethod
    def ngram_history(self, tg_id: int):
        return self.NGRAM_HISTORY.format(tg_id=tg_id)
    
    @classmethod
    def message_count(self, tg_id: int):
        return self.MESSAGE_COUNT.format(tg_id=tg_id)

class ActivityStore(BaseStore):
    hashs_cls = ActivityHashs
    hashs: type[ActivityHashs]

    async def exist_cooldown(self, tg_id: int):
        key = self.hashs.cooldown(tg_id)
        return await self.client.exists(key)
         
    async def get_lrange_history(self, tg_id: int, history_size: int):
        key = self.hashs.ngram_history(tg_id)
        return await self.client.lrange(key, 0, history_size - 1)

    async def update(self, tg_id: int, sec: int, units: list, history_size: int, dedup_ttl: int):
        cd_key = self.hashs.cooldown(tg_id)
        hist_key = self.hashs.ngram_history(tg_id)
        await self.client.set(cd_key, "1", ex=sec)
        await self.client.lpush(hist_key, json.dumps(units, ensure_ascii=False))
        await self.client.ltrim(hist_key, 0, history_size - 1)
        await self.client.expire(hist_key, dedup_ttl)

    async def message_incr(self, tg_id: int, count: int = 1):
        key = self.hashs.message_count(tg_id)
        return await self.client.incr(key, count)