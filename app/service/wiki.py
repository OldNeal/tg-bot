from app.service.base import BaseService
from app.logic.wiki import WikiLogic
from app.validate.args import SearchArg, NameArg
from app.aio.cls.msg.wiki import WikiText
from app.aio.cls.buttons.wiki import WikiIKB
from app.aio.cls.fsm.utils import WikiFSM

class WikiService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = WikiLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.IKB = WikiIKB(tg_id=self.tg_id)
        self.text = WikiText
        self.state = WikiFSM(state)
    
    async def ga(self):
        await self.state.update_data(back_where='ga')
        if self.enter_args and self.kwargs.get('value'):
            return await self.search_ga(**SearchArg.model_validate(self.kwargs).model_dump())
        else:
            return await self.all_gas()

    async def all_gas(self, group: str | None = None):
        data = await self.logic.all_gas()
        group = group or list({g.group for g in data.gas})[0]
        await self.state.update_data(group=group, is_all=True)
        return self.to_json([
            [self.text.ga(data).all, data, self.IKB.all_gas(data.gas, group=group)]
            ])

    async def search_ga(self, value: str):
        data = await self.logic.search_ga(value)
        await self.state.update_data(value=value, is_all=False)
        return self.to_json([
            [self.text.ga.search(value, len(data.gas) if data.gas else 0), data, self.IKB.gas(data.gas) if data.gas else None]
            ])

    async def get_ga(self, id: int | None = None, where: str = 'gas'):
        if id is None:
            id = await self.state.get_value('ga_id')
        data = await self.logic.ga(id=id)
        if len(data.paths) == 1:
            return await self.get_path(data.paths[0].path_id, where)
        await self.state.update_data(ga_id=id)
        return self.to_json([
            [self.text.ga(data).info(), data, self.IKB.ga(data.paths, where)]
            ])
    
    async def back_ga(self):
        is_all = await self.state.get_value('is_all')
        if is_all:
            group = await self.state.get_value('group')
            return await self.all_gas(group)
        else:
            value = await self.state.get_value('value')
            return await self.search_ga(value)

    async def path(self):
        await self.state.update_data(back_where='paths')
        if self.enter_args and self.kwargs.get('value'):
            return await self.search_path(**SearchArg.model_validate(self.kwargs).model_dump())
        else:
            return await self.all_paths()

    async def get_path(self, id: int, where: str | None = None):
        data = await self.logic.path(id=id)
        value = await self.state.get_value('value')
        back_where = where or await self.state.get_value('back_where')
        return self.to_json([
            [self.text.path(data).info(value), data, self.IKB.back(back_where)]
            ])

    async def all_paths(self, group: str | None = None):
        data = await self.logic.all_paths()
        group = group or list({p.group for p in data.paths})[0]
        await self.state.update_data(group=group, is_all=True)
        return self.to_json([
            [self.text.path(data).all, data, self.IKB.all_paths(data.paths, group=group)]
            ])

    async def search_path(self, value: str):
        data = await self.logic.search_path(value)
        await self.state.update_data(value=value, is_all=False)
        return self.to_json([
            [self.text.path.search(value, len(data.paths) if data.paths else 0), data, self.IKB.paths(data.paths) if data.paths else None]
            ])

    async def back_path(self):
        is_all = await self.state.get_value('is_all')
        if is_all:
            group = await self.state.get_value('group')
            return await self.all_paths(group)
        else:
            value = await self.state.get_value('value')
            return await self.search_path(value)
            

