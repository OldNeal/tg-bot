from app.logic.base import BaseLogic
from app.logic.utils import class_decor


@class_decor
class ActivityLogic(BaseLogic):
    async def activity(self, message_count: int = 1):
        return await self.client.activity_points(await self.body, message_count)

    async def points(self, message_count: int | None = None):
        return await self.client.client.config.activity_points(await self.body, message_count)

    async def add_points(
        self,
        purpose_tg_id: int,
        points: int,
        reason: str | None = None,
    ):
        user_id = await self.get_user_id(purpose_tg_id)
        return await self.client.activity_points_add(
            await self.body,
            user_id,
            points,
            reason,
        )

    async def deduct_points(
        self,
        purpose_tg_id: int,
        points: int,
        reason: str | None = None,
    ):
        user_id = await self.get_user_id(purpose_tg_id)
        return await self.client.activity_points_deduct(
            await self.body,
            user_id,
            points,
            reason,
        )

    async def reset_points(self, purpose_tg_id: int, reason: str | None = None):
        user_id = await self.get_user_id(purpose_tg_id)
        return await self.client.activity_points_reset(
            await self.body,
            user_id,
            reason,
        )

    async def reset_limit(self, purpose_tg_id: int):
        user_id = await self.get_user_id(purpose_tg_id)
        return await self.client.activity_points_limit_reset(await self.body, user_id)
