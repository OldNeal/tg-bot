import json
import json5
from typing import Literal

from app.logic.news_paper import NewsPaperLogic
from app.exception.base import JSONEnterError
from app.api.schemas import AnswerAllNewsPaperInfo, AnswerNewsPaperInfoReaders
from app.service.base import AnswerBody, BaseService
from app.tg.buttons.news_paper import NewsPaperIKB
from app.tg.fsm.state import NewsPaperState
from app.tg.fsm.utils import NewsPaperFSM
from app.tg.text.news_paper import NewsPaperText

class NewsPaperAction:
    subscribe = 'subscribe'
    unsubscribe = 'unsubscribe'
    notify = 'notify'
    make_editor = 'make_editor'
    fire_editor = 'fire_editor'

    @property
    def literal(self):
        return Literal[NewsPaperAction.subscribe, NewsPaperAction.unsubscribe, NewsPaperAction.notify, NewsPaperAction.make_editor, NewsPaperAction.fire_editor]


class NewsPaperService(BaseService):
    logic_class: type[NewsPaperLogic] = NewsPaperLogic
    logic: NewsPaperLogic
    text_class: type[NewsPaperText] = NewsPaperText
    text: type[NewsPaperText]
    ikb_class: type[NewsPaperIKB] = NewsPaperIKB
    IKB: NewsPaperIKB
    fsm_class: type[NewsPaperFSM] = NewsPaperFSM
    fsm: NewsPaperFSM

    async def menu(self):
        return await self.answer([
            AnswerBody(
                text=self.text.menu(),
                reply_markup=self.IKB.menu(),
            )
        ])

    async def search(self, value: str | None = None, page: int | None = None):
        value = value or await self.fsm.get_value('search_value')
        if not value:
            return await self.to_enter_search()
        page = page if page is not None else await self.fsm.get_value('page', 0)
        data = await self.logic.search(name=value)
        return await self._show_news_papers(data, 'search', page, value)

    async def _show_news_papers(
        self,
        data: AnswerAllNewsPaperInfo,
        mode: Literal['search', 'all', 'list', 'editors'],
        page: int,
        value: str | None = None,
    ):
        news_papers = data.news_papers
        pages = self.to_pages(news_papers)
        max_page = len(pages)
        if max_page == 0 or page < 0 or page >= max_page:
            page = 0
        if mode == 'search':
            search_value = data.search_value or value
            if search_value is None:
                raise ValueError('Не указан поисковый запрос для списка газет')
            text = self.text.search(search_value, len(news_papers), page, max_page)
            await self.fsm.update_data(
                mode=mode,
                page=page,
                search_value=search_value,
            )
        elif mode in {'all', 'list'}:
            text = self.text.news_papers(len(news_papers), page, max_page)
            await self.fsm.update_data(mode=mode, page=page)
        else:
            text = self.text.editors(len(news_papers), page, max_page)
            await self.fsm.update_data(mode=mode, page=page)
        current_page = pages[page] if pages else []
        return await self.answer([
            AnswerBody(
                text=text,
                data=data,
                reply_markup=self.IKB.news_papers(
                    current_page,
                    page,
                    max_page,
                    mode,
                ),
            )
        ])

    async def to_enter_search(self):
        await self.fsm.set_state(NewsPaperState.search)
        await self.fsm.save_message(self.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_search(),
                reply_markup=self.IKB.cancel(),
            )
        ])

    async def to_search(self):
        await self.fsm.remove_value('search_value')
        return await self.search(value=self.message.text, page=0)

    async def _page_for_mode(
        self,
        mode: Literal['all', 'list', 'editors'],
        page: int | None,
    ):
        if page is not None:
            return page
        if await self.fsm.get_value('mode') == mode:
            return await self.fsm.get_value('page', 0)
        return 0

    async def all(self, page: int | None = None):
        page = await self._page_for_mode('all', page)
        data = await self.logic.all()
        return await self._show_news_papers(data, 'all', page)
    
    async def list(self, page: int | None = None):
        page = await self._page_for_mode('list', page)
        data = await self.logic.list()
        return await self._show_news_papers(data, 'list', page)

    async def editors(self, page: int | None = None):
        page = await self._page_for_mode('editors', page)
        data = await self.logic.editors()
        return await self._show_news_papers(data, 'editors', page)

    async def info(self, news_paper_id: int):
        data = await self.logic.info(news_paper_id)
        mode = await self.fsm.get_value('mode', 'search')
        page = await self.fsm.get_value('page', 0)
        return await self.answer([
            AnswerBody(
                text=self.text.info(data.news_paper),
                data=data,
                reply_markup=self.IKB.news_paper_info(
                    news_paper_id,
                    for_buttons=data.for_buttons,
                    mode=mode,
                    page=page,
                ),
            )
        ])

    async def capture(self, news_paper_id: int):
        data = await self.logic.capture(news_paper_id)
        mode = await self.fsm.get_value('mode', 'search')
        page = await self.fsm.get_value('page', 0)
        return await self.answer([
            AnswerBody(
                text=self.text.capture(data.news_paper),
                data=data,
                reply_markup=(
                    self.IKB.news_paper_info(
                        news_paper_id,
                        for_buttons=data.for_buttons,
                        mode=mode,
                        page=page,
                    )
                    if data.for_buttons is not None
                    else None
                ),
            )
        ])

    async def get_settings(self, news_paper_id: int | None = None):
        if news_paper_id is None:
            news_paper_id = await self.fsm.get_value('news_paper_id')
        if news_paper_id is None:
            raise ValueError('Не указан ID газеты для настроек')

        await self.fsm.set_state()
        await self.fsm.update_data(news_paper_id=news_paper_id)
        data = await self.logic.settings_values(news_paper_id)
        return await self.answer([
            AnswerBody(
                text=self.text.settings_values(data.values),
                data=data,
                reply_markup=self.IKB.settings_values(
                    news_paper_id,
                    self.is_bot_message,
                ),
            )
        ])

    async def default_settings(self, news_paper_id: int | None = None):
        if news_paper_id is None:
            news_paper_id = await self.fsm.get_value('news_paper_id')
        if news_paper_id is None:
            raise ValueError('Не указан ID газеты для настроек')
        await self.logic.settings_default(news_paper_id, is_all=True)
        await self.callback.answer('⚙️ Настройки сброшены')
        return await self.get_settings(news_paper_id)

    async def to_redact_settings(self, news_paper_id: int | None = None):
        if news_paper_id is None:
            news_paper_id = await self.fsm.get_value('news_paper_id')
        if news_paper_id is None:
            raise ValueError('Не указан ID газеты для настроек')
        await self.fsm.update_data(news_paper_id=news_paper_id)
        await self.fsm.set_state(NewsPaperState.settings)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_enter_settings(),
                reply_markup=self.IKB.back_to_settings(news_paper_id),
            )
        ])

    async def redact_settings(self):
        news_paper_id = await self.fsm.get_value('news_paper_id')
        if news_paper_id is None:
            raise ValueError('Не указан ID газеты для настроек')
        try:
            parametrs = json5.loads(self.message.text)
        except (json.JSONDecodeError, ValueError) as error:
            raise JSONEnterError(
                'Ввел невалидный json',
                json=self.message.text,
            ) from error
        await self.logic.settings_redact(news_paper_id, parametrs)
        return await self.get_settings(news_paper_id)

    async def readers(self, news_paper_id: int, page: int | None = None):
        if page is None:
            current_news_paper_id = await self.fsm.get_value('news_paper_id')
            page = (
                await self.fsm.get_value('readers_page', 0)
                if current_news_paper_id == news_paper_id
                else 0
            )
        return await self._show_readers(news_paper_id, page)

    async def select_news_paper(
        self,
        action: NewsPaperAction.literal,
        page: int = 0,
        purpose_tg_id: int | None = None,
    ):
        if purpose_tg_id is not None:
            await self.fsm.update_data(action_purpose_tg_id=purpose_tg_id)
        elif await self.fsm.get_value('action_purpose_tg_id') is None:
            await self.fsm.update_data(action_purpose_tg_id=self.logic.purpose_tg_id)

        if action == NewsPaperAction.subscribe:
            data = await self.logic.for_subscribe()
        elif action == NewsPaperAction.unsubscribe:
            data = await self.logic.list()
        else:
            data = await self.logic.editors()  
        pages = self.to_pages(data.news_papers)
        max_page = len(pages)
        if max_page == 0 or page < 0 or page >= max_page:
            page = 0
        return await self.answer([
            AnswerBody(
                text=self.text.choose_news_paper(action, len(data.news_papers), page, max_page),
                data=data,
                reply_markup=self.IKB.news_papers(
                    pages[page] if pages else [],
                    page,
                    max_page,
                    action,
                ),
            )
        ])

    async def run_news_paper_action(self, action: NewsPaperAction.literal, news_paper_id: int):
        if action == NewsPaperAction.subscribe:
            return await self.subscribe(news_paper_id)
        if action == NewsPaperAction.unsubscribe:
            return await self.unsubscribe(news_paper_id)
        if action == NewsPaperAction.notify:
                reply_message_id = await self.fsm.pop_value('reply_message_id')
                result = await self.notify(news_paper_id, reply_message_id)
                if reply_message_id:
                    await self.message.delete()
                return result
        purpose_tg_id = await self.fsm.get_value(
            'action_purpose_tg_id',
            self.logic.purpose_tg_id,
        )
        if action == NewsPaperAction.make_editor:
            return await self.make_editor(news_paper_id, purpose_tg_id)
        return await self.fire_editor(news_paper_id, purpose_tg_id)

    async def _show_readers(self, news_paper_id: int, page: int):
        data: AnswerNewsPaperInfoReaders = await self.logic.readers(news_paper_id)
        pages = self.to_pages(data.readers)
        max_page = len(pages)
        if page < 0 or page >= max_page:
            page = 0
        current_page = pages[page] if pages else []
        await self.fsm.update_data(
            news_paper_id=news_paper_id,
            readers_page=page
        )
        return await self.answer([
            AnswerBody(
                text=self.text.readers(data.name, page, max_page),
                data=data,
                reply_markup=self.IKB.readers(current_page, news_paper_id, page, max_page),
            )
        ])

    async def reader(self, news_paper_id: int, purpose_tg_id: int):
        readers_page = await self.fsm.get_value('readers_page', 0)
        data = await self.logic.reader(news_paper_id, purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.reader(data),
                data=data,
                reply_markup=self.IKB.reader(
                    news_paper_id,
                    readers_page,
                    purpose_tg_id,
                    data.for_buttons,
                ),
            )
        ])

    async def to_give(self, news_paper_id: int, purpose_tg_id: int):
        data = await self.logic.reader(news_paper_id, purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_give(data),
                data=data,
                reply_markup=self.IKB.give_news_paper(news_paper_id, purpose_tg_id),
            )
        ])

    async def give(self, news_paper_id: int, purpose_tg_id: int):
        data = await self.logic.give(news_paper_id, purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.give(data),
                data=data,
                reply_markup=self.IKB.back_to_reader(
                    news_paper_id,
                    purpose_tg_id,
                ),
            )
        ])
    
    async def create(self, name: str | None = None):
        if name:
            data = await self.logic.create(name=name)
            return await self.answer([
                AnswerBody(
                    text=self.text.created(data.news_paper),
                    data=data,
                    reply_markup=self.IKB.create(data.news_paper.id),
                    is_rich_text=True,
                )
            ])
        return await self.to_enter_name_for_create()

    async def to_enter_name_for_create(self):
        await self.fsm.set_state(NewsPaperState.create)
        await self.fsm.save_message(self.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_create(),
                reply_markup=self.IKB.cancel(),
            )
        ])

    async def enter_name_for_create(self):
        return await self.create(self.message.text)

    async def subscribe(self, news_paper_id: int | None = None):
        if news_paper_id is None:
            return await self.select_news_paper('subscribe')
        data = await self.logic.subscribe(news_paper_id)
        return await self.answer([
            AnswerBody(
                text=self.text.sub(self.tg_id, data.news_paper.name),
                reply_markup=self.IKB.back_to_info(data.news_paper.id),
            )
        ])
    
    async def unsubscribe(self, news_paper_id: int | None = None):
        if news_paper_id is None:
            return await self.select_news_paper('unsubscribe')
        data = await self.logic.unsubscribe(news_paper_id)
        return await self.answer([
            AnswerBody(
                text=self.text.unsub(self.tg_id, data.news_paper.name),
                reply_markup=self.IKB.back_to_info(data.news_paper.id),
            )
        ])

    async def to_unsubscribe(self, news_paper_id: int):
        data = await self.logic.info(news_paper_id)
        return await self.answer([
            AnswerBody(
                text=self.text.confirm_unsub(data.news_paper),
                data=data,
                reply_markup=self.IKB.confirm_unsubscribe(news_paper_id),
            )
        ])

    
    async def notify(self, news_paper_id: int | None = None, reply_message_id: int | None = None):
        if self.message.reply_to_message:
            reply_message_id = self.message.reply_to_message.message_id
            await self.fsm.update_data(reply_message_id=reply_message_id)
        if news_paper_id is None:
            return await self.select_news_paper('notify')
        data = await self.logic.notify(news_paper_id)
        return await self.answer([
            AnswerBody(
                text=self.text.notify({r.user.tg_id:r.user.fullname for r in readers}),
                reply_message_id=reply_message_id
            ) for readers in self.to_pages(data.readers)
        ])
    
    async def to_notify(self, news_paper_id: int):
        return await self.answer([
            AnswerBody(
                text=self.text.to_notify(news_paper_id),
                reply_markup=self.IKB.back_to_info(news_paper_id)
            )
        ])

    async def make_editor(self, news_paper_id: int, purpose_tg_id: int):
        data = await self.logic.make_editor(news_paper_id, purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.make(self.tg_id, data.user.tg_id, data.user.fullname, data.news_paper.name),
                reply_markup=self.IKB.back_to_reader(data.news_paper.id, data.user.tg_id),
            )
        ])

    async def fire_editor(self, news_paper_id: int, purpose_tg_id: int):
        data = await self.logic.fire_editor(news_paper_id, purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.fire(self.tg_id, data.user.tg_id, data.user.fullname, data.news_paper.name),
                reply_markup=self.IKB.back_to_reader(data.news_paper.id, data.user.tg_id),
            )
        ])
