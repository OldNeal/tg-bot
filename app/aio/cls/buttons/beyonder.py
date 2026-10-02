from app.aio.cls.buttons.base import BotIKB, MenuCall
from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.cls.callback.beyonder import DrinkCall, BeyonderBackCall, KillCall, BeyonderInfoCall, BeyonderListPageCall
from app.aio.cls.callback.wiki import PathCall
from app.validate.api import AnswerBeyonderInfo

class BeyonderIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=BeyonderBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def accert_kill(self, purpose_tg_id: int):
        self.builder.button(text='✅ Да', callback_data=KillCall(accert=True, purpose_tg_id=(purpose_tg_id or self.tg_id), tg_id=self.tg_id))
        self.builder.button(text='❌ Нет', callback_data=KillCall(cancel=True, purpose_tg_id=(purpose_tg_id or self.tg_id), tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def list(self, datas: list[AnswerBeyonderInfo], page: int, max_page: int, path_id: int):
        for data in datas:
            self.builder.button(text=f'{data.beyonder.seq if data.beyonder.seq >= 0 else '🏵'} - {data.user.fullname or data.user.username or 'Неизвестный'}', callback_data=BeyonderInfoCall(purpose_tg_id=data.user.tg_id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=BeyonderListPageCall(page=page-1, path_id=path_id, tg_id=self.tg_id).pack()))
        if page != max_page - 1 and max_page != 0:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=BeyonderListPageCall(page=page+1, path_id=path_id, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)        
        self.builder.row(InlineKeyboardButton(text=f'↩️ Назад', callback_data=PathCall(id=path_id, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()   