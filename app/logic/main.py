from app.logic.base import BaseLogic
from app.logic.utils import class_decor

@class_decor
class MainLogic(BaseLogic):
    async def user_settings(self):
        return await self.client.user_settings(await self.body)

    async def user_settings_values(self):
        return await self.client.user_settings_values(await self.body)

    async def user_settings_redact(self, data: dict):
        body = await self.body
        return await self.client.user_settings_redact(self.schemas.QueryUserSetting.model_validate(
            body.model_dump() | {'parametrs': data}
        ))

    async def user_settings_default(self, parametr: str | None = None, is_all: bool = False):
        body = await self.body
        return await self.client.user_settings_default(self.schemas.QueryUserSettingDefault.model_validate(
            body.model_dump() | {
                'to_default': self.schemas.UserSettingDefault(
                    parametr=parametr,
                    group=None,
                    is_all=is_all,
                )
            }
        ))

    async def users_list(self, page: int | None = None, per_page: int | None = None):
        return await self.client.user_list(page=page, per_page=per_page)
    
    async def users_search(self, page: int | None = None, per_page: int | None = None, **criteria: int | str):
        return await self.client.user_search(page=page, per_page=per_page, **criteria)

    async def user_delete(self, user_id: int):
        return await self.client.user_delete(await self.body, user_id)

    async def user_info(self, user_id: int):
        return await self.client.get_info(self.check_is_not_none(user_id, await self.get_user_id(self.purpose_tg_id)))

    async def beyonder_sistem_info(self):
        return await self.client.beyonder_sistem_info()
