from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.aio.cls.callback.base import MenuCall, CancelCall

class BotIKB:
    def __init__(self, tg_id: int):
        self.builder = InlineKeyboardBuilder()
        self.tg_id = tg_id
 
    def another_tg_id(self, tg_id: int):
        self.tg_id = tg_id
        return self

    def cancel(self):
        self.builder.button(text='❌ Отменить', callback_data=CancelCall(tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
 