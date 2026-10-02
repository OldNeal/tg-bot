from app.service.base import BaseService
from app.logic.stats import StatsLogic
from app.aio.cls.msg.stats import StatsText
from app.validate.args import SearchArg
from app.aio.cls.buttons.stats import StatsIKB

class StatsService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = StatsLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = StatsText
        self.IKB = StatsIKB(self.tg_id)

    async def all(self):
        args = SearchArg.model_validate(self.kwargs)
        if args.value:
            return await self.beyonders(**args.model_dump())
        data = await self.logic.all()
        return self.to_json([
            [self.text.all(data), data, None]
            ])

    async def beyonders(self, value: str, page: int = 0):
        data = await self.logic.search_path(value)
        pages = self.to_pages(data.paths)
        max_page = len(pages)
        if page >= max_page:
            page = 0
        return self.to_json([
            [self.text.search(max_page, page, value, len(data.paths)), data, self.IKB.paths((pages[page] if len(pages) > 0 else []), max_page, page)]
            ])