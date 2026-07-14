from app.service.base import BaseService
from app.logic.main import MainLogic
from app.aio.cls.msg.main import MainText

class MainService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = MainLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = MainText

    async def info(self):
        data = await self.logic.info(self.kwargs.get('tg_id'))
        return [
            ['Держи карточку', None],
            [self.text(data).info, None]
            ]

