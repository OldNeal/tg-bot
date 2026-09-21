from app.service.base import BaseService
from app.logic.main import MainLogic
from app.aio.cls.msg.main import MainText
from app.aio.cls.buttons.main import MainIKB

class MainService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = MainLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = MainText
        self.IKB = MainIKB(tg_id=self.tg_id)

    async def info(self):
        data = await self.logic.info(self.kwargs.get('purpose_tg_id'))
        return self.to_json([
            [self.text(data).first_msg_by_info, None, None],
            [self.text(data).info, data, None]
            ])

    async def ping(self):
        api_ping = await self.logic.test_api_connect()
        return [
            [self.text.check_ping(api_ping), None]
        ]
    
    async def my_state(self):
        data = await self.state.state.get_data()
        self.msg_to_json = True
        self.msg_to_json_keyboard = False
        return self.to_json([
            [self.text.html(data), data, self.IKB.my_state()]
            ])

    async def my_state_clear(self):
        data = await self.state.state.clear()
        return self.to_json([
            [self.text.state_clear(), data, None]
            ])

    async def my_state_pop(self):
        data = await self.state.state.get_data()
        key = self.command.args
        if key in data:
            data.pop(key)
            await self.state.state.set_data(data)
            return self.to_json([
                [self.text.state_pop(), data, None]
                ])
        return self.to_json([
            [self.text.state_dont_pop(), data, None]
            ])     