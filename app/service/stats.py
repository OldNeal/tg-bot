from app.service.base import BaseService, AnswerBody
from app.logic.stats import StatsLogic
from app.tg.text.stats import StatsText
from app.tg.buttons.stats import StatsIKB
from app.tg.callback.back_values import StatsBackValues
from app.tg.fsm.state import StatsState
from app.tg.fsm.utils import StatsFSM

class StatsService(BaseService):
    logic_class: type[StatsLogic] = StatsLogic
    logic: StatsLogic
    text_class: type[StatsText] = StatsText
    text: type[StatsText]
    ikb_class: type[StatsIKB] = StatsIKB
    IKB: StatsIKB
    fsm_class: type[StatsFSM] = StatsFSM
    fsm: StatsFSM

    async def all(self, value: str | None = None):
        if value:
            return await self.paths(value=value)
        data = await self.logic.all()
        return await self.answer([
            AnswerBody(
                text=self.text.all(data),
                data=data,
                reply_markup=self.IKB.all(),
                is_rich_text=True,
            )
        ])

    async def paths(self, value: str | None = None, page: int | None = None):
        value = value or await self.fsm.get_value('value')
        if value is None:
            return await self.to_enter_path()
        page = page if page is not None else await self.fsm.get_value('page', 0)
        data = await self.logic.search_path(value)
        pages = self.to_pages(data.paths)
        max_page = len(pages)
        if page >= max_page:
            page = 0
        await self.fsm.update_data(value=value, page=page)
        return await self.answer([
            AnswerBody(
                text=self.text.search(
                    max_page,
                    page,
                    value,
                    len(data.paths) if data.paths else 0
                ),
                data=data,
                reply_markup=self.IKB.paths(
                    pages[page] if pages else [],
                    max_page,
                    page,
                    value,
                    where=StatsBackValues.all
                ),
                is_rich_text=True,
            )
        ])

    async def to_enter_path(self):
        await self.fsm.set_state(StatsState.search)
        await self.fsm.save_message(self.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.enter_search_value(),
                reply_markup=self.IKB.back(StatsBackValues.all),
                is_rich_text=True,
            )
        ])

    async def enter_path(self):
        msg0 = await self.fsm.get_message()
        await self.paths(self.message.text, 0)
        await self.fsm.set_state()
        await self.bot.delete_message(*msg0)
        await self.fsm.remove_message()

    async def back_paths(self):
        await self.fsm.remove_value('value')
        return await self.paths()
