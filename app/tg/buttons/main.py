from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.callback.main import MainBackCall, MyStateCall

class MainIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=MainBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def my_state(self):
        self.builder.button(text='🔄️ Обновить', callback_data=MyStateCall(tg_id=self.tg_id))
        return self.builder.as_markup()