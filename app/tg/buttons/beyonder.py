from aiogram.types import InlineKeyboardButton, DisabledButton

from app.tg.buttons.base import BotIKB
from app.tg.callback.back_values import BeyonderBackValues
from app.tg.callback.base import BackCall
from app.tg.callback.main import MainInfoCall
from app.tg.callback.beyonder import (
    BeyonderBackCall,
    BeyonderInfoCall,
    BeyonderListPageCall,
    BeyonderTimeInfoCall,
    BeyonderUpSeqCall,
    DrinkCall,
    KillCall,
)
from app.tg.callback.wiki import PathCall
from app.validate.api import AnswerBeyonderInfo, AnswerPathInfo


class BeyonderIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=BeyonderBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def info_card(self, data: AnswerBeyonderInfo, where: str | None = None):
        purpose = data.purpose
        if purpose is None or purpose.telegram is None:
            return self.builder.as_markup()

        telegram = purpose.telegram
        if telegram.tg_id == self.tg_id:
            if data.beyonder is None:
                self.builder.button(text='🧪 Выпить зелье', callback_data=DrinkCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id, seq=9))
            if data.beyonder:
                if data.beyonder.seq >= 0:
                    self.builder.button(text='🚀 Продвинуться', callback_data=BeyonderUpSeqCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id))
                self.builder.button(text='⏱ Дата продвижения', callback_data=BeyonderTimeInfoCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id))
                self.builder.button(text='☠️ Потерять контроль', callback_data=KillCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id))
        if where:
            self.builder.button(text='↩️ Назад', callback_data=BeyonderBackCall(where=where, tg_id=self.tg_id))
        self.builder.button(
            text='💳 Главная карточка',
            callback_data=MainInfoCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def accert_kill(self, purpose_tg_id: int):
        self.builder.button(text='✅ Да', callback_data=KillCall(accert=True, purpose_tg_id=(purpose_tg_id or self.tg_id), tg_id=self.tg_id))
        self.builder.button(text='❌ Нет', callback_data=KillCall(cancel=True, purpose_tg_id=(purpose_tg_id or self.tg_id), tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def confirm_upseq(self, paths: list[AnswerPathInfo], path_id: int, purpose_tg_id: int, seq: int | None = None):
        for path in sorted(paths, key=lambda item: item.path_id):
            self.builder.button(
                text=f'{"✅ " if path.path_id == path_id else ""}{path.name}',
                icon_custom_emoji_id=path.custom_emodzi_id,
                callback_data=BeyonderUpSeqCall(
                    purpose_tg_id=purpose_tg_id,
                    path_id=path.path_id,
                    seq=seq,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.adjust(3, 2)
        self.builder.row(*[InlineKeyboardButton(
            text='✅ Продвинуться',
            callback_data=BeyonderUpSeqCall(
                purpose_tg_id=purpose_tg_id,
                path_id=path_id,
                seq=seq,
                confirmed=True,
                tg_id=self.tg_id,
            ).pack(),
        ),
        InlineKeyboardButton(
            text='❌ Отмена',
            callback_data=BeyonderUpSeqCall(
                purpose_tg_id=purpose_tg_id,
                confirmed=False,
                tg_id=self.tg_id,
            ).pack(),
        )], width=1)
        return self.builder.as_markup()

    def list(self, datas: list[AnswerBeyonderInfo], page: int, max_page: int, path_id: int, where: str | None = None):
        for data in datas:
            telegram = data.purpose.telegram if data.purpose else None
            if telegram is None:
                continue
            name = data.purpose.name or telegram.fullname or telegram.username or 'Неизвестный'
            seq_text = data.beyonder.seq if data.beyonder and data.beyonder.seq is not None else '🏵'
            self.builder.button(text=f'{seq_text if seq_text >= 0 else '🏵'} - {name}', callback_data=BeyonderInfoCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            page_back = page - 10
            pages.append(InlineKeyboardButton(text='⏪', callback_data=BeyonderListPageCall(page=page_back if page_back > 0 else 0, path_id=path_id, where=where, tg_id=self.tg_id).pack()))
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=BeyonderListPageCall(page=page-1, path_id=path_id, where=where, tg_id=self.tg_id).pack()))
        else:
            pages.append(InlineKeyboardButton(text='⏪', disabled=DisabledButton()))
            pages.append(InlineKeyboardButton(text='⬅️', disabled=DisabledButton()))
        if page < max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=BeyonderListPageCall(page=page+1, path_id=path_id, where=where, tg_id=self.tg_id).pack()))
            page_next = page + 10
            pages.append(InlineKeyboardButton(text='⏩', callback_data=BeyonderListPageCall(page=page_next if page_next < max_page - 1 else max_page - 1, path_id=path_id, where=where, tg_id=self.tg_id).pack()))
        else:
            pages.append(InlineKeyboardButton(text='➡️', disabled=DisabledButton()))
            pages.append(InlineKeyboardButton(text='⏩', disabled=DisabledButton()))
        self.builder.row(*pages)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=BackCall(where=where, tg_id=self.tg_id).pack()))
        else:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=PathCall(id=path_id, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()

    def back_to_card(self, purpose_tg_id: int):
        return self.builder.button(text='↩️ Назад', callback_data=BeyonderInfoCall(purpose_tg_id=purpose_tg_id, tg_id=self.tg_id)).as_markup()
