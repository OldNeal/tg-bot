from app.logic.base import BaseLogic
from app.logic.utils import class_decor


@class_decor
class NewsPaperLogic(BaseLogic):
    async def search(self, name: str, page: int | None = None):
        return await self.client.news_paper_search(name, page=page)

    async def all(self, page: int | None = None):
        return await self.client.news_paper_all(await self.body, page=page)
    
    async def list(self, page: int | None = None):
        return await self.client.news_paper_list(await self.body, page=page)

    async def editors(self, page: int | None = None):
        return await self.client.news_paper_list_where_editor(await self.body, page=page)
    
    async def for_subscribe(self, page: int | None = None):
        return await self.client.news_paper_for_subscribe(await self.body, page=page)

    async def info(self, news_paper_id: int):
        return await self.client.news_paper_info(await self.body, news_paper_id)

    async def info_description(self, news_paper_id: int):
        return await self.client.news_paper_info_description(await self.body, news_paper_id)

    async def capture(self, news_paper_id: int):
        return await self.client.news_paper_capture(await self.body, news_paper_id)

    async def readers(self, news_paper_id: int, page: int | None = None):
        return await self.client.news_paper_readers(await self.body, news_paper_id, page=page)
    
    async def reader(self, news_paper_id: int, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.news_paper_reader(await self.body, news_paper_id, user_id)

    async def create(self, name: str):
        return await self.client.news_paper_create(await self.body, name)

    async def subscribe(self, news_paper_id: int):
        return await self.client.news_paper_subscribe(await self.body, news_paper_id)

    async def unsubscribe(self, news_paper_id: int):
        return await self.client.news_paper_unsubscribe(await self.body, news_paper_id)

    async def notify(self, news_paper_id: int):
        return await self.client.news_paper_notify(await self.body, news_paper_id)

    async def make_editor(self, news_paper_id: int, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.news_paper_make_editor(await self.body, news_paper_id, user_id)

    async def fire_editor(self, news_paper_id: int, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.news_paper_fire_editor(await self.body, news_paper_id, user_id)

    async def give(self, news_paper_id: int, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.news_paper_give(
            await self.body,
            news_paper_id,
            user_id,
        )

    async def settings(self, news_paper_id: int):
        return await self.client.news_paper_settings(await self.body, news_paper_id)

    async def settings_values(self, news_paper_id: int):
        return await self.client.news_paper_settings_values(await self.body, news_paper_id)

    async def settings_redact(self, news_paper_id: int, parametrs: dict):
        body = await self.body
        data = self.schemas.QueryNewsPaperSetting.model_validate(
            body.model_dump() | {'parametrs': parametrs}
        )
        return await self.client.news_paper_settings_redact(data, news_paper_id)

    async def settings_default(
        self,
        news_paper_id: int,
        parametr: str | None = None,
        group: str | None = None,
        is_all: bool = False,
    ):
        body = await self.body
        data = self.schemas.QueryNewsPaperSettingDefault.model_validate(
            body.model_dump()
            | {
                'to_default': self.schemas.OrganSettingDefault(
                    parametr=parametr,
                    group=group,
                    is_all=is_all,
                )
            }
        )
        return await self.client.news_paper_settings_default(data, news_paper_id)
