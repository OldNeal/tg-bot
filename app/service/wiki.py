from app.service.base import BaseService, AnswerBody
from app.logic.wiki import WikiLogic
from app.tg.text.wiki import WikiText
from app.tg.buttons.wiki import WikiIKB
from app.tg.fsm.utils import WikiFSM, BeyonderFSM
from app.tg.fsm.state import WikiState
from app.tg.callback.back_values import WikiBackValues

class WikiService(BaseService):
    logic_class: type[WikiLogic] = WikiLogic
    logic: WikiLogic
    text_class: type[WikiText] = WikiText
    text: type[WikiText]
    ikb_class: type[WikiIKB] = WikiIKB
    IKB: WikiIKB
    fsm_class: type[WikiFSM] = WikiFSM
    fsm: WikiFSM

    async def menu(self, wiki_type: str = 'path'):
        wiki_type = wiki_type or await self.fsm.get_value('type', 'path')
        await self.fsm.update_data(type=wiki_type, from_menu=1)
        return await self.answer([
            AnswerBody(
                text=self.text.menu(),
                reply_markup=self.IKB.menu(wiki_type),
            )
        ])

    async def ga(self, value: str | None = None):
        await self.fsm.update_data(back_where=WikiBackValues.ga)
        if value:
            return await self.search_ga(value)
        return await self.all_gas()

    async def all_gas(self, group: str | None = None, where: str | None = None):
        data = await self.logic.all_gas()
        group = group or list({g.group for g in data.gas if g.group.lower().startswith('зем')})[0]
        await self.fsm.update_data(group=group, is_all=True)
        return await self.answer([
            AnswerBody(
                text=self.text.ga(data).all,
                data=data,
                reply_markup=self.IKB.all_gas(data.gas, group=group, where=where),
            )
        ])

    async def search_ga(self, value: str | None = None, page: int | None = None, where: str | None = None):
        if not value:
            return await self.to_enter_search_value('ga')
        page = page if page is not None else await self.fsm.get_value('page', 0)
        data = await self.logic.search_ga(value, page=page)
        max_page = data.page.max
        page = data.page.number
        await self.fsm.update_data(back_where=WikiBackValues.search, page=page, value=value, is_all=False)
        return await self.answer([
            AnswerBody(
                text=self.text.ga.search(max_page, page, value, data.count),
                data=data,
                reply_markup=(
                    self.IKB.gas(data.gas, max_page, page, value, where=where)
                    if data.gas
                    else self.IKB.search('ga')
                ),
            )
        ])

    async def get_ga(self, id: int | None = None, where: str = WikiBackValues.gas):
        if id is None:
            id = await self.fsm.get_value('ga_id')
        data = await self.logic.ga(id=id)
        if len(data.paths) == 1:
            return await self.get_path(data.paths[0].path_id, where)
        await self.fsm.update_data(ga_id=id)
        return await self.answer([
            AnswerBody(
                text=self.text.ga(data).info(),
                data=data,
                reply_markup=self.IKB.ga(data.paths, where),
            )
        ])

    async def back_ga(self, is_all: bool | None = None):
        is_all = await self.fsm.get_value('is_all', is_all)
        if self.is_bot_message and await self.fsm.get_value('from_menu'):
            back_where = WikiBackValues.menu
        else:
            back_where = None
            await self.fsm.pop_value('from_menu')
        if is_all:
            group = await self.fsm.get_value('group')
            return await self.all_gas(group, where=back_where)
        value = await self.fsm.get_value('value')
        return await self.search_ga(value, where=back_where)

    async def path(self, value: str | None = None):
        await self.fsm.update_data(back_where=WikiBackValues.paths)
        if value:
            return await self.search_path(value)
        return await self.all_paths()

    async def get_path(self, id: int, where: str | None = None):
        data = await self.logic.path(id=id)
        value = await self.fsm.get_value('value')
        back_where = where or await self.fsm.get_value('back_where')
        await BeyonderFSM(self.fsm.state).pop_value('page')
        return await self.answer([
            AnswerBody(
                text=self.text.path(data).info(value),
                data=data,
                reply_markup=self.IKB.path(data.path_id, back_where),
            )
        ])

    async def all_paths(self, group: str | None = None, where: str | None = None):
        data = await self.logic.all_paths()
        group = group or list({p.group for p in data.paths if p.group.lower().startswith('зем')})[0]
        await self.fsm.update_data(group=group, is_all=True)
        return await self.answer([
            AnswerBody(
                text=self.text.path(data).all,
                data=data,
                reply_markup=self.IKB.all_paths(data.paths, group=group, where=where),
            )
        ])

    async def search_path(self, value: str | None = None, page: int | None = None, where: str | None = None):
        if not value:
            return await self.to_enter_search_value('path')
        page = page if page is not None else await self.fsm.get_value('page', 0)
        data = await self.logic.search_path(value, page=page)
        max_page = data.page.max
        page = data.page.number
        await self.fsm.update_data(back_where=WikiBackValues.search, page=page, value=value, is_all=False)
        return await self.answer([
            AnswerBody(
                text=self.text.path.search(max_page, page, value, data.count),
                data=data,
                reply_markup=(
                    self.IKB.paths(data.paths, max_page, page, value, where=where)
                    if data.paths
                    else self.IKB.search('path')
                ),
            )
        ])

    async def back_path(self, is_all: bool | None = None):
        is_all = is_all if is_all is not None else await self.fsm.get_value('is_all')
        if self.is_bot_message and await self.fsm.get_value('from_menu'):
            back_where = WikiBackValues.menu
        else:
            back_where = None
            await self.fsm.pop_value('from_menu')
        if is_all:
            group = await self.fsm.get_value('group')
            return await self.all_paths(group, where=back_where)
        value = await self.fsm.get_value('value')
        return await self.search_path(value, where=back_where)

    async def to_enter_search_value(self, search_type: str):
        await self.fsm.set_state(WikiState.search)
        await self.fsm.update_data(search_type=search_type)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.enter_search_value(),
                reply_markup=self.IKB.enter_search(self.is_bot_message),
            )
        ])

    async def enter_search_value(self):
        msg0 = await self.fsm.get_message()
        search_type = await self.fsm.get_value('search_type', 'path')
        if search_type == 'path':
            await self.search_path(self.message.text, page=0)
        else:
            await self.search_ga(self.message.text, page=0)
        await self.fsm.set_state()
        await self.bot.delete_message(*msg0)
        await self.fsm.remove_message()
