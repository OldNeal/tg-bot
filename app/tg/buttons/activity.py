from aiogram.types import InlineKeyboardButton, DisabledButton

from app.tg.buttons.base import BotIKB
from app.tg.callback.items import ItemInfoCall

class ActivityIKB(BotIKB):
    def back_to_items(
        self,
        item_id: int,
        source: str,
        page: int
    ):
        self.builder.button(
                text='↩️ Назад',
                callback_data=ItemInfoCall(
                    item_id=item_id,
                    source=source,
                    page=page,
                    tg_id=self.tg_id,
                ),
            )
        return self.builder.as_markup()