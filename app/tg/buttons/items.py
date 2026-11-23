from aiogram.types import DisabledButton, InlineKeyboardButton

from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.callback.main import MainInfoCall
from app.tg.callback.items import (
    ItemInfoCall,
    ItemInventoryPageCall,
    ItemQuantityCall,
    ItemsPageCall,
    ItemActionCall
)
from app.validate.core import AnswerInventory, AnswerItems, ItemInfo, Page

ACTIVITY_POINTS_TAG = 'activity_point'

class ItemIKB(BotIKB):
    def _item(self, item: ItemInfo, source: str, page: int):
        quantity = f' ({item.quantity} шт.)' if item.quantity and item.quantity > 1 else ''
        self.builder.button(
            text=f'{item.emodzi or "📦"} {item.name[:30]}{quantity}',
            callback_data=ItemInfoCall(
                item_id=item.item_id,
                source=source,
                page=page,
                owned_quantity=item.quantity if source == 'inventory' else None,
                tg_id=self.tg_id,
            ),
        )

    def _pages(self, page: Page | None, callback_type: type[ItemInventoryPageCall] | type[ItemsPageCall]):
        if page is None or page.max <= 1:
            return

        buttons = []
        if page.number > 0:
            buttons.append(InlineKeyboardButton(
                text='⬅️',
                callback_data=callback_type(page=page.number - 1, tg_id=self.tg_id).pack(),
            ))
        else:
            buttons.append(InlineKeyboardButton(text='⬅️', disabled=DisabledButton()))

        if page.number < page.max - 1:
            buttons.append(InlineKeyboardButton(
                text='➡️',
                callback_data=callback_type(page=page.number + 1, tg_id=self.tg_id).pack(),
            ))
        else:
            buttons.append(InlineKeyboardButton(text='➡️', disabled=DisabledButton()))

        self.builder.row(*buttons)

    def inventory(self, data: AnswerInventory):
        for item in data.items:
            self._item(item, 'inventory', data.page.number if data.page else 0)
        if data.items:
            self.builder.adjust(1)
        self._pages(data.page, ItemInventoryPageCall)
        self.builder.row(InlineKeyboardButton(
            text='↩️ К карточке',
            callback_data=MainInfoCall(purpose_tg_id=self.tg_id, tg_id=self.tg_id).pack(),
        ))
        return self.builder.as_markup()

    def items(self, data: AnswerItems):
        for item in data.items:
            self._item(item, 'items', data.page.number if data.page else 0)
        if data.items:
            self.builder.adjust(1)
        self._pages(data.page, ItemsPageCall)
        self.builder.row(InlineKeyboardButton(
            text='↩️ В главное меню', 
            callback_data=MenuCall(where='main', tg_id=self.tg_id).pack()
            ))
        return self.builder.as_markup()

    def item_info(
        self,
        item: ItemInfo,
        source: str,
        page: int,
        is_admin: bool,
        owned_quantity: int | None = None,
    ):
        if is_admin:
            self.builder.button(
                text='➕',
                callback_data=ItemQuantityCall(
                    item_id=item.item_id,
                    source=source,
                    page=page,
                    owned_quantity=owned_quantity,
                    action='give',
                    tg_id=self.tg_id,
                ),
            )
            self.builder.button(
                text='➖',
                callback_data=ItemQuantityCall(
                    item_id=item.item_id,
                    source=source,
                    page=page,
                    owned_quantity=owned_quantity,
                    action='take',
                    tg_id=self.tg_id,
                ),
            )
        if item.tag == ACTIVITY_POINTS_TAG:
            
            self.builder.button(
                text='⚡ Лимиты активности',
                callback_data=ItemActionCall(
                    item_id=item.item_id,
                    source=source,
                    page=page,
                    owned_quantity=owned_quantity,
                    action='activity_limits',
                    tg_id=self.tg_id,
                ),
            )
        
        self.builder.adjust(2, 1)
        if source == 'inventory':
            back_call = ItemInventoryPageCall(page=page, tg_id=self.tg_id).pack()
            back_text = '↩️ В инвентарь'
        else:
            back_call = ItemsPageCall(page=page, tg_id=self.tg_id).pack()
            back_text = '↩️ К каталогу'
        self.builder.row(InlineKeyboardButton(text=back_text, callback_data=back_call))
        return self.builder.as_markup()

    def quantity_cancel(self, item_id: int, source: str, page: int, owned_quantity: int | None = None):
        return self.builder.button(
            text='↩️ К предмету',
            callback_data=ItemInfoCall(
                item_id=item_id,
                source=source,
                page=page,
                owned_quantity=owned_quantity,
                tg_id=self.tg_id,
            ),
        ).as_markup()
