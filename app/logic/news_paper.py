from app.logic.base import BaseLogic
from app.logic.utils import class_decor


@class_decor
class NewsPaperLogic(BaseLogic):
    async def search(self, name: str):
        return await self.client.news_paper_search(name)

    async def all(self):
        return await self.client.news_paper_all(self.body)
    
    async def list(self):
        return await self.client.news_paper_list(self.body)

    async def editors(self):
        return await self.client.news_paper_list_where_editor(self.body)
    
    async def for_subscribe(self):
        return await self.client.news_paper_for_subscribe(self.body)

    async def info(self, news_paper_id: int):
        return await self.client.news_paper_info(self.body, news_paper_id)

    async def info_description(self, news_paper_id: int):
        return await self.client.news_paper_info_description(self.body, news_paper_id)

    async def capture(self, news_paper_id: int):
        return await self.client.news_paper_capture(self.body, news_paper_id)

    async def readers(self, news_paper_id: int):
        return await self.client.news_paper_readers(self.body, news_paper_id)
    
    async def reader(self, news_paper_id: int, purpose_tg_id: int | None = None):
        return await self.client.news_paper_reader(self.body, news_paper_id, purpose_tg_id or self.purpose_tg_id)

    async def create(self, name: str):
        return await self.client.news_paper_create(self.body, name)

    async def subscribe(self, news_paper_id: int):
        return await self.client.news_paper_subscribe(self.body, news_paper_id)

    async def unsubscribe(self, news_paper_id: int):
        return await self.client.news_paper_unsubscribe(self.body, news_paper_id)

    async def notify(self, news_paper_id: int):
        return await self.client.news_paper_notify(self.body, news_paper_id)

    async def make_editor(self, news_paper_id: int, purpose_tg_id: int | None = None):
        return await self.client.news_paper_make_editor(self.body, news_paper_id, purpose_tg_id or self.purpose_tg_id)

    async def fire_editor(self, news_paper_id: int, purpose_tg_id: int | None = None):
        return await self.client.news_paper_fire_editor(self.body, news_paper_id, purpose_tg_id or self.purpose_tg_id)

    async def give(self, news_paper_id: int, purpose_tg_id: int | None = None):
        return await self.client.news_paper_give(
            self.body,
            news_paper_id,
            purpose_tg_id or self.purpose_tg_id,
        )

    async def settings(self, news_paper_id: int):
        return await self.client.news_paper_settings(self.body, news_paper_id)

    async def settings_values(self, news_paper_id: int):
        return await self.client.news_paper_settings_values(self.body, news_paper_id)

    async def settings_redact(self, news_paper_id: int, parametrs: dict):
        data = self.schemas.QueryNewsPaperSetting.model_validate(
            self.body.model_dump() | {'parametrs': parametrs}
        )
        return await self.client.news_paper_settings_redact(data, news_paper_id)

    async def settings_default(
        self,
        news_paper_id: int,
        parametr: str | None = None,
        group: str | None = None,
        is_all: bool = False,
    ):
        data = self.schemas.QueryNewsPaperSettingDefault.model_validate(
            self.body.model_dump()
            | {
                'to_default': self.schemas.OrganSettingDefault(
                    parametr=parametr,
                    group=group,
                    is_all=is_all,
                )
            }
        )
        return await self.client.news_paper_settings_default(data, news_paper_id)
