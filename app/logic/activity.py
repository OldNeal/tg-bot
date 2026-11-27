from app.logic.base import BaseLogic
from app.logic.utils import class_decor


@class_decor
class ActivityLogic(BaseLogic):
    async def activity(self, message_count: int = 1):
        return await self.client.activity_points(await self.body, message_count)

    async def activity_reset(self, purpose_tg_id: int):
        user_id = await self.get_user_id(purpose_tg_id)
        return await self.client.activity_points_limit_reset(await self.body, user_id)

    async def activity_reset_global(self):
        return await self.client.activity_points_limit_reset_global(await self.body)

    async def limits(self):
        return await self.client.activity_points_limit(await self.user_id)
