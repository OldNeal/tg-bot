from app.aio.cls.buttons.base import BotIKB, MenuCall
from app.validate.api import AnswerAllPathInfo, AnswerPathInfo, AnswerGAInfo
from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.cls.callback.beyonder import DrinkCall, BeyonderBackCall, KillCall

class BeyonderIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=BeyonderBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def accert_kill(self, purpose_tg_id: int):
        self.builder.button(text='✅ Да', callback_data=KillCall(accert=True, purpose_tg_id=(purpose_tg_id or self.tg_id), tg_id=self.tg_id))
        self.builder.button(text='❌ Нет', callback_data=KillCall(cancel=True, purpose_tg_id=(purpose_tg_id or self.tg_id), tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()