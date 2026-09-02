from app.service.base import BaseService
from app.logic.stats import StatsLogic
from app.aio.cls.msg.stats import StatsText

class StatsService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = StatsLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = StatsText

    async def all(self):
        data = await self.logic.all()
        return self.to_json([
            [self.text.all(data), data, None]
            ])
