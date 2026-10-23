from aiogram.filters import CommandObject

from app.service.base import BaseService, AnswerBody
from app.logic.main import MainLogic
from app.tg.text.main import MainText
from app.tg.buttons.main import MainIKB
from app.tg.fsm.utils import FSMUtils

class MainService(BaseService):
    logic_class: type[MainLogic] = MainLogic
    logic: MainLogic
    text_class: type[MainText] = MainText
    text: type[MainText]
    ikb_class: type[MainIKB] = MainIKB
    IKB: MainIKB
    fsm: FSMUtils

    async def info(self, purpose_tg_id: int | None = None):
        data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).first_msg_by_info,
            ),
            AnswerBody(
                text=self.text(data).info,
                data=data,
            )
        ])

    async def ping(self):
        api_ping = await self.logic.test_api_connect()
        return await self.answer([
            AnswerBody(text=self.text.check_ping(api_ping), is_rich_text=True)
        ])

    async def my_state(self):
        data = await self.fsm.get_data()
        return await self.answer([
            AnswerBody(
                text=self.text.json(data),
                data=None,
                reply_markup=self.IKB.my_state(),
                is_rich_text=True,
            )
        ])

    async def my_state_clear(self):
        data = await self.fsm.clear()
        return await self.answer([
            AnswerBody(
                text=self.text.state_clear(),
                data=None,
                is_rich_text=True,
            )
        ])

    async def my_state_pop(self, command: CommandObject):
        data = await self.fsm.get_data()
        key = command.args
        if key in data:
            data.pop(key)
            await self.fsm.set_data(data)
            text = self.text.state_pop()
        else:
            text = self.text.state_dont_pop()
        return await self.answer([
            AnswerBody(text=text, data=None, is_rich_text=True)
        ])
