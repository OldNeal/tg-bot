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
        return self.to_json([
            [self.text(data).first_msg_by_info, None, None],
            [self.text(data).info, data, None]
            ])

    async def ping(self):
        api_ping = await self.logic.test_api_connect()
        return [
            [self.text.check_ping(api_ping), None]
        ]