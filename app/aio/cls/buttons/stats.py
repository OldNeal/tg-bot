from app.aio.cls.buttons.base import BotIKB, MenuCall, CancelCall
from app.aio.cls.callback.stats import StatsBackCall, StatsPageCall
from app.aio.cls.callback.beyonder import BeyonderListPageCall
from app.validate.api import AnswerPathInfo
from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

class StatsIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id)).as_markup()
        
    def paths(self, paths: list[AnswerPathInfo], max_page: int, page: int, where: str | None = None):
        for path in sorted(paths, key=lambda x: x.path_id):
            self.builder.button(text=path.name, icon_custom_emoji_id=path.custom_emodzi_id, callback_data=BeyonderListPageCall(path_id=path.path_id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=StatsPageCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1 and max_page != 0:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=StatsPageCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)    
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
