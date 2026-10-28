from datetime import datetime, timedelta

from app.logic.base import BaseLogic
from app.logic.utils import class_decor

@class_decor
class BeyonderLogic(BaseLogic):
    async def info(self, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_info(user_id)

    async def path(self, name: str | None = None, id: int | None = None):
        return await self.client.get_path(name=name, id=id)

    async def ga(self, name: str | None = None, id: int | None = None):
        return await self.client.get_ga(name=name, id=id)

    async def drink(self, purpose_tg_id: int | None = None, path_name: str | None = None, path_id: int | None = None, seq: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_drink(await self.body, user_id, path_name, path_id, seq)

    async def upseq(self, purpose_tg_id: int | None = None, path_name: str | None = None, seq: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_upseq(await self.body, user_id, path_name, seq)

    async def dowseq(self, purpose_tg_id: int | None = None, path_name: str | None = None, seq: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_dowseq(await self.body, user_id, path_name, seq)
    
    async def kill(self, purpose_tg_id: int | None = None, is_admin: bool = False):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        body = (await self.body).model_copy(update={'is_admin': is_admin})
        return await self.client.beyonder_kill(body, user_id)

    async def time_info(self, purpose_tg_id: int | None = None, to_raise: bool | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_time_info(user_id, to_raise)
    
    async def time_redact(self, duration: timedelta, operator: str = '+', purpose_tg_id: int | None = None):
        seconds = duration.total_seconds()
        if seconds < 0:
            operator = '-'
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_time_redact(await self.body, abs(seconds), operator, user_id)
    
    async def time_replace(self, datetime_arg: datetime, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.beyonder_time_replace(await self.body, datetime_arg.isoformat(), user_id)

    async def list(self, path_id: int):
        return await self.client.beyonder_list(path_id)
