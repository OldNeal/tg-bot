from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.callback.beyonder import BeyonderInfoCall
from app.tg.callback.main import MainBackCall, MyStateCall
from app.tg.callback.organ import OrganMemberCall
from app.validate.api import AnswerBaseInfo

class MainIKB(BotIKB):    
    def menu(self):
        self.builder.button(text='💳 Моя карточка', callback_data=MenuCall(where='info', tg_id=self.tg_id))
        self.builder.button(text='🏛️ Организации', callback_data=MenuCall(where='organ', tg_id=self.tg_id))
        self.builder.button(text='📰 Газеты', callback_data=MenuCall(where='newspaper', tg_id=self.tg_id))
        self.builder.button(text='📚 Вики', callback_data=MenuCall(where='wiki', tg_id=self.tg_id))
        self.builder.button(text='📊 Статистика', callback_data=MenuCall(where='stats', tg_id=self.tg_id))
        self.builder.button(text='❔ Справка', callback_data=MenuCall(where='help', tg_id=self.tg_id))
        return self.builder.adjust(2, 2, 2).as_markup()

    def info(self, data: AnswerBaseInfo):
        purpose = data.purpose
        telegram = purpose.telegram if purpose else None
        if telegram is None:
            return self.builder.as_markup()

        if data.member:
            self.builder.button(
                text='🏛 Карточка участника',
                callback_data=OrganMemberCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id),
            )
        self.builder.button(
            text='🔮 Карточка потустороннего',
            callback_data=BeyonderInfoCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=MainBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def my_state(self):
        self.builder.button(text='🔄️ Обновить', callback_data=MyStateCall(tg_id=self.tg_id))
        return self.builder.as_markup()