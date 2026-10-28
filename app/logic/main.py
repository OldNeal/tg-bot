from app.logic.base import BaseLogic
from app.logic.utils import class_decor
from app.api.client import get_info, user_delete, user_list, user_search

@class_decor
class MainLogic(BaseLogic):
    async def users_list(self):
        return await user_list()

    async def users_search(self, **criteria: int | str):
        return await user_search(**criteria)

    async def user_delete(self, user_id: int):
        return await user_delete(await self.body, user_id)

    async def user_info(self, user_id: int):
        return await get_info(self.check_is_not_none(user_id, await self.get_user_id(self.purpose_tg_id)))