from app.service.base import BaseService
from app.logic.wiki import WikiLogic
from app.validate.args import SearchArg, NameArg


class WikiService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = WikiLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        
    async def group(self):
        if self.enter_args:
            data = await self.logic.search_group(**NameArg.model_validate(self.kwargs).model_dump())
        else:
            data = await self.logic.all_groups()
        return [
            data.model_dump_json(), None
            ]
    
    async def ga(self):
        if self.enter_args:
            data = await self.logic.search_ga(**SearchArg.model_validate(self.kwargs).model_dump())
        else:
            data = await self.logic.all_gas()
        return [
            data.model_dump_json(), None
            ]

    async def path(self):
        if self.enter_args:
            data = await self.logic.search_path(**SearchArg.model_validate(self.kwargs).model_dump())
        else:
            data = await self.logic.all_paths()
        return [
            data.model_dump_json(), None
            ]

    async def get_ga(self, name: str | None = None, id: int | None = None):
        data = await self.logic.ga(name, id)
        return [
            data.model_dump_json(), None
            ]  

    async def get_path(self, name: str | None = None, id: int | None = None):
        data = await self.logic.path(name, id)
        return [
            data.model_dump_json(), None
            ]      
        