from app.logic.base import BaseLogic
from app.logic.utils import class_decor

@class_decor
class MainLogic(BaseLogic):
    async def users_list(self, page: int | None = None, per_page: int | None = None):
        return await self.client.user_list(page=page, per_page=per_page)
    
    async def users_search(self, page: int | None = None, per_page: int | None = None, **criteria: int | str):
        return await self.client.user_search(page=page, per_page=per_page, **criteria)

    async def user_delete(self, user_id: int):
        return await self.client.user_delete(await self.body, user_id)

    async def user_info(self, user_id: int):
        return await self.client.get_info(self.check_is_not_none(user_id, await self.get_user_id(self.purpose_tg_id)))
