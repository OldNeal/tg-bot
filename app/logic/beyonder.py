from app.logic.base import BaseLogic
from app.logic.utils import class_decor
from datetime import datetime, timedelta

@class_decor
class BeyonderLogic(BaseLogic):
    async def drink(self, purpose_tg_id: int | None = None, path_name: str | None = None, seq: int | None = None):
        return await self.client.drink(self.body, (purpose_tg_id or self.purpose_tg_id), path_name, seq)

    async def upseq(self, purpose_tg_id: int | None = None, path_name: str | None = None, seq: int | None = None):
        return await self.client.upseq(self.body, purpose_tg_id or self.purpose_tg_id, path_name, seq)

    async def dowseq(self, purpose_tg_id: int | None = None, path_name: str | None = None, seq: int | None = None):
        return await self.client.dowseq(self.body, purpose_tg_id or self.purpose_tg_id, path_name, seq)
    
    async def kill(self, purpose_tg_id: int | None = None):
        return await self.client.kill(self.body, purpose_tg_id or self.purpose_tg_id)

    async def time_info(self, purpose_tg_id: int | None = None):
        return await self.client.time_info(purpose_tg_id or self.purpose_tg_id)
    
    async def time_redact(self, duration: timedelta, operator: str = '+', purpose_tg_id: int | None = None):
        seconds = duration.total_seconds()
        if seconds < 0:
            operator = '-'
        return await self.client.time_redact(self.body, abs(seconds), operator, (purpose_tg_id or self.purpose_tg_id))
    
    async def time_replace(self, datetime_arg: datetime, purpose_tg_id: int | None = None):
        return await self.client.time_replace(self.body, datetime_arg.isoformat(), (purpose_tg_id or self.purpose_tg_id))