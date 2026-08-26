from app.logic.base import BaseLogic
from app.logic.utils import class_decor
from datetime import datetime, timedelta
from app.validate.api import QueryOrganSetting, QueryOrganSettingDefault, OrganSettingDefault

@class_decor
class OrganLogic(BaseLogic):
    async def member(self, purpose_tg_id: int | None = None):
        return await self.client.organ_member(self.body, purpose_tg_id or self.purpose_tg_id)

    async def search(self, value: str):
        return await self.client.organ_search(value)

    async def info(self, organ_id: int | None = None, purpose_tg_id: int | None = None):
        return await self.client.organ_info(self.body, organ_id, (purpose_tg_id or self.purpose_tg_id))

    async def info_members(self, organ_id: int | None = None, purpose_tg_id: int | None = None):
        return await self.client.organ_info_members(self.body, organ_id, (purpose_tg_id or self.purpose_tg_id))

    async def info_description(self, organ_id: int | None = None, purpose_tg_id: int | None = None):
        return await self.client.organ_info_description(self.body, organ_id, (purpose_tg_id or self.purpose_tg_id))
    
    async def list(self):
        return await self.client.organ_list()

    async def top_members(self):
        return await self.client.organ_top_members()
    
    async def top_days(self):
        return await self.client.organ_top_days()




    async def login(self, organ_id: int | None = None):
        return await self.client.organ_login(self.body, organ_id)

    async def exit(self):
        return await self.client.organ_exit(self.body)
    
    async def create(self, name: str):
        return await self.client.organ_create(self.body, name)

    async def settings(self):
        return await self.client.organ_settings_values(self.body)

    async def settings_redact(self, data: dict):
        return await self.client.organ_settings_redact(QueryOrganSetting.model_validate(self.body.model_dump() | {
            'parametrs':data
            }))

    async def settings_default(self, parametr: str | None = None, group: str | None = None, is_all: bool = False,):
        return await self.client.organ_settings_default(QueryOrganSettingDefault.model_validate(self.body.model_dump() | {
            'to_default':OrganSettingDefault(parametr=parametr, group=group, is_all=is_all)
            }))

    async def capture(self):
        return await self.client.organ_capture(self.body)




    async def uprank(self, purpose_tg_id: int | None = None, rank: int | None = None):
        return await self.client.organ_uprank(self.body, (purpose_tg_id or self.purpose_tg_id), rank)

    async def downrank(self, purpose_tg_id: int | None = None, rank: int | None = None):
        return await self.client.organ_downrank(self.body, (purpose_tg_id or self.purpose_tg_id), rank)

    async def kick(self, purpose_tg_id: int):
        return await self.client.organ_kick(self.body, purpose_tg_id)
    
    async def titul_redact(self, purpose_tg_id: int | None = None, titul: str | None = None):
        return await self.client.organ_titul_redact(self.body, (purpose_tg_id or self.purpose_tg_id), titul)
    
    async def titul_delete(self, purpose_tg_id: int | None = None):
        return await self.client.organ_titul_delete(self.body, (purpose_tg_id or self.purpose_tg_id))
    
    async def give(self, purpose_tg_id: int | None = None):
        return await self.client.organ_give(self.body, (purpose_tg_id or self.purpose_tg_id))