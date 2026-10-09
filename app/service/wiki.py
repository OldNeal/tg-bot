from app.service.base import BaseService
from app.logic.wiki import WikiLogic
from app.validate.args import SearchArg, NameArg
from app.aio.cls.msg.wiki import WikiText
from app.aio.cls.buttons.wiki import WikiIKB
from app.aio.cls.fsm.utils import WikiFSM, BeyonderFSM
from app.aio.cls.fsm.state import WikiState
from app.aio.cls.callback.back import WikiBackValues

class WikiService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = WikiLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.IKB = WikiIKB(tg_id=self.tg_id)
        self.text = WikiText
        self.state = WikiFSM(state)

    async def menu(self, wiki_type: str = 'path'):
        wiki_type = wiki_type or await self.state.get_value('type', 'path')
        await self.state.update_data(type=wiki_type, from_menu=1)
        return self.to_json([
            [self.text.menu(), None, self.IKB.menu(wiki_type)]
            ])
    
    async def ga(self):
        await self.state.update_data(back_where=WikiBackValues.ga)
        if self.enter_args and self.kwargs.get('value'):
            return await self.search_ga(**SearchArg.model_validate(self.kwargs).model_dump())
        else:
            return await self.all_gas()

    async def all_gas(self, group: str | None = None, where: str | None = None):
        data = await self.logic.all_gas()
        group = group or list({g.group for g in data.gas if g.group.lower().startswith('зем')})[0]
        await self.state.update_data(group=group, is_all=True)
        return self.to_json([
            [self.text.ga(data).all, data, self.IKB.all_gas(data.gas, group=group, where=where)]
            ])

    async def search_ga(self, value: str | None = None, page: int | None = None, where: str | None = None):
        if value:
            data = await self.logic.search_ga(value)
        else:
            return await self.to_enter_search_value('ga')
        page = page if not(page is None) else await self.state.get_value('page', 0)
        pages = self.to_pages(data.gas)
        max_page = len(pages)
        if page >= max_page:
            page = 0
        await self.state.update_data(back_where=WikiBackValues.search, page=page, value=value, is_all=False)
        return self.to_json([
            [self.text.ga.search(max_page, page, value, (len(data.gas) if data.gas else 0)), data, self.IKB.gas(pages[page], max_page, page, value, where=where) if data.gas else self.IKB.search('ga')]
            ])

    async def get_ga(self, id: int | None = None, where: str = WikiBackValues.gas):
        if id is None:
            id = await self.state.get_value('ga_id')
        data = await self.logic.ga(id=id)
        if len(data.paths) == 1:
            return await self.get_path(data.paths[0].path_id, where)
        await self.state.update_data(ga_id=id)
        return self.to_json([
            [self.text.ga(data).info(), data, self.IKB.ga(data.paths, where)]
            ])
    
    async def back_ga(self, is_all: bool | None = None):
        is_all = await self.state.get_value('is_all', is_all)
        if self.is_bot_message and await self.state.get_value('from_menu'):
            back_where = WikiBackValues.menu  
        else:
            back_where = None
            await self.state.pop_value('from_menu')
        if is_all:
            group = await self.state.get_value('group')
            return await self.all_gas(group, where=back_where)
        else:
            value = await self.state.get_value('value')
            return await self.search_ga(value, where=back_where)

    async def path(self):
        await self.state.update_data(back_where=WikiBackValues.paths)
        if self.enter_args and self.kwargs.get('value'):
            return await self.search_path(**SearchArg.model_validate(self.kwargs).model_dump())
        else:
            return await self.all_paths()

    async def get_path(self, id: int, where: str | None = None):
        data = await self.logic.path(id=id)
        value = await self.state.get_value('value')
        back_where = where or await self.state.get_value('back_where')
        await BeyonderFSM(self.state.state).pop_value('page')
        return self.to_json([
            [self.text.path(data).info(value), data, self.IKB.path(data.path_id, back_where)]
            ])

    async def all_paths(self, group: str | None = None, where: str | None = None):
        data = await self.logic.all_paths()
        group = group or list({p.group for p in data.paths if p.group.lower().startswith('зем')})[0]
        await self.state.update_data(group=group, is_all=True)
        return self.to_json([
            [self.text.path(data).all, data, self.IKB.all_paths(data.paths, group=group, where=where)]
            ])

    async def search_path(self, value: str | None = None, page: int | None = None, where: str | None = None):
        if value:
            data = await self.logic.search_path(value)
        else:
            return await self.to_enter_search_value('path')
        page = page if not(page is None) else await self.state.get_value('page', 0)
        pages = self.to_pages(data.paths)
        max_page = len(pages)
        if page >= max_page:
            page = 0
        await self.state.update_data(back_where=WikiBackValues.search, page=page, value=value, is_all=False)
        return self.to_json([
            [self.text.path.search(max_page, page, value, (len(data.paths) if data.paths else 0)), data, self.IKB.paths(pages[page], max_page, page, value, where=where) if data.paths else self.IKB.search('path')]
            ])

    async def back_path(self, is_all: bool | None = None):
        is_all = is_all if not is_all is None else await self.state.get_value('is_all')
        if self.is_bot_message and await self.state.get_value('from_menu'):
            back_where = WikiBackValues.menu  
        else:
            back_where = None
            await self.state.pop_value('from_menu')
        if is_all:
            group = await self.state.get_value('group')
            return await self.all_paths(group, where=back_where)
        else:
            value = await self.state.get_value('value')
            return await self.search_path(value, where=back_where)

    async def to_enter_search_value(self, search_type: str):
        await self.state.set_state(WikiState.search)
        await self.state.update_data(search_type=search_type)
        await self.state.save_message(self.message.chat.id, self.message.message_id)
        return self.to_json([
            [self.text.enter_search_value(), None, self.IKB.enter_search(self.is_bot_message)]
            ])

    async def enter_search_value(self):
        search_type = await self.state.get_value('search_type', 'path')
        if search_type == 'path':
            return await self.search_path(self.message.text)
        else:
            return await self.search_ga(self.message.text)
