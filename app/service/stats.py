from app.service.base import BaseService
from app.logic.stats import StatsLogic
from app.aio.cls.msg.stats import StatsText
from app.validate.args import SearchArg
from app.aio.cls.buttons.stats import StatsIKB
from app.aio.cls.callback.back import StatsBackValues
from app.aio.cls.fsm.state import StatsState
from app.aio.cls.fsm.utils import StatsFSM

class StatsService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = StatsLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = StatsText
        self.IKB = StatsIKB(self.tg_id)
        self.state = StatsFSM(state)

    async def all(self):
        args = SearchArg.model_validate(self.kwargs)
        if args.value:
            return await self.paths(**args.model_dump())
        data = await self.logic.all()
        return self.to_json([
            [self.text.all(data), data, self.IKB.all()]
            ])

    async def paths(self, value: str | None = None, page: int | None = None):
        value = value or await self.state.get_value('value')
        if value is None:
            return await self.to_enter_path()
        page = page if not(page is None) else await self.state.get_value('page', 0)
        data = await self.logic.search_path(value)
        pages = self.to_pages(data.paths)
        max_page = len(pages)
        if page >= max_page:
            page = 0
        await self.state.update_data(value=value, page=page)
        return self.to_json([
            [self.text.search(max_page, page, value, (len(data.paths) if data.paths else 0)), data, self.IKB.paths((pages[page] if len(pages) > 0 else []), max_page, page, value, where=StatsBackValues.all)]
            ])

    async def to_enter_path(self):
        await self.state.set_state(StatsState.search)
        await self.state.save_message(self.chat.id, self.message.message_id)
        return self.to_json([
            [self.text.enter_search_value(), None, self.IKB.back(StatsBackValues.all)]
            ])

    async def enter_path(self):
        await self.state.set_state()
        return await self.paths(self.message.text, 0)

    async def back_paths(self):
        await self.state.remove_value('value')
        return await self.paths()