from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup, DisabledButton

from app.tg.buttons.base import BotIKB, MenuCall, CancelCall
from app.tg.callback.stats import StatsBackCall, StatsPageCall, StatsPathsCall
from app.tg.callback.beyonder import BeyonderListPageCall
from app.tg.callback.back_values import StatsBackValues
from app.validate.api import AnswerPathInfo

class StatsIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def all(self):
        self.builder.button(text='🔍 Статистика путей', callback_data=StatsPathsCall(tg_id=self.tg_id))
        self.builder.button(text='↩️ В главное меню', callback_data=MenuCall(where='main', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
        
    def paths(self, paths: list[AnswerPathInfo], max_page: int, page: int, value: str, where: str | None = None):
        for path in sorted(paths, key=lambda x: x.path_id):
            self.builder.button(text=path.name, icon_custom_emoji_id=path.custom_emodzi_id, callback_data=BeyonderListPageCall(path_id=path.path_id, page=0, where=StatsBackValues.stats_paths, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            page_back = page - 10
            pages.append(InlineKeyboardButton(text='⏪', callback_data=StatsPageCall(page=page_back if page_back > 0 else 0, value=value, tg_id=self.tg_id).pack()))
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=StatsPageCall(page=page-1, value=value, tg_id=self.tg_id).pack()))
        else:
            pages.append(InlineKeyboardButton(text='⏪', disabled=DisabledButton()))
            pages.append(InlineKeyboardButton(text='⬅️', disabled=DisabledButton()))
        if page < max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=StatsPageCall(page=page+1, value=value, tg_id=self.tg_id).pack()))
            page_next = page + 10
            pages.append(InlineKeyboardButton(text='⏩', callback_data=StatsPageCall(page=page_next if page_next < max_page - 1 else max_page - 1, value=value, tg_id=self.tg_id).pack()))
        else:
            pages.append(InlineKeyboardButton(text='➡️', disabled=DisabledButton()))
            pages.append(InlineKeyboardButton(text='⏩', disabled=DisabledButton()))
        self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='🔍 Поискать ещё раз', callback_data=StatsPathsCall(tg_id=self.tg_id).pack()))
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
