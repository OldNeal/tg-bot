from app.service.base import BaseService, AnswerBody
from app.logic.main import MainLogic
from app.tg.text.help import HelpText
from app.tg.buttons.help import HelpIKB
from app.tg.fsm.utils import FSMUtils

class HelpService(BaseService):
    logic_class: type[MainLogic] = MainLogic
    logic: MainLogic
    text_class: type[HelpText] = HelpText
    text: type[HelpText]
    ikb_class: type[HelpIKB] = HelpIKB
    IKB: HelpIKB
    fsm: FSMUtils

    async def main(self):
        return await self.answer([
            AnswerBody(
                text=self.text.main(),
                reply_markup=self.IKB.main(),
            )
        ])
