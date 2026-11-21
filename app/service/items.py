from typing import Literal

from app.exception.base import PermissionError
from app.exception.items import ItemCommandStateError, ItemCommandValueError
from app.logic.items import ItemLogic
from app.service.base import AnswerBody, BaseService
from app.tg.buttons.items import ItemIKB
from app.tg.fsm.state import ItemState
from app.tg.fsm.utils import ItemFSM
from app.tg.text.items import ItemText


class ItemService(BaseService):
    logic_class: type[ItemLogic] = ItemLogic
    logic: ItemLogic
    text_class: type[ItemText] = ItemText
    text: type[ItemText]
    ikb_class: type[ItemIKB] = ItemIKB
    IKB: ItemIKB
    fsm_class: type[ItemFSM] = ItemFSM
    fsm: ItemFSM

    @staticmethod
    def _validate_item_context(item_id: int, source: str, page: int):
        if item_id <= 0 or source not in ('inventory', 'items') or page < 0:
            raise ItemCommandValueError()

    async def inventory(self, page: int = 0):
        data = await self.logic.inventory(page=page)
        return await self.answer([
            AnswerBody(
                text=self.text.inventory(data),
                data=data,
                reply_markup=self.IKB.inventory(data),
            )
        ])

    async def items(self, page: int = 0):
        data = await self.logic.items(page=page)
        return await self.answer([
            AnswerBody(
                text=self.text.items(data),
                data=data,
                reply_markup=self.IKB.items(data),
            )
        ])

    async def item_info(
        self,
        item_id: int,
        source: str,
        page: int,
        owned_quantity: int | None = None
    ):
        self._validate_item_context(item_id, source, page)
        await self.fsm.set_state()
        await self.fsm.clear_this_state()
        item = await self.logic.item_info(item_id, source=source)
        return await self.answer([
            AnswerBody(
                text=self.text.item_info(item),
                data=item,
                reply_markup=self.IKB.item_info(
                    item=item,
                    source=source,
                    page=page,
                    is_admin=self.tg_id_in_admins,
                    owned_quantity=owned_quantity,
                ),
            )
        ])

    async def start_quantity_input(
        self,
        item_id: int,
        action: Literal['give', 'take'],
        source: str,
        page: int,
        owned_quantity: int | None = None,
    ):
        if not self.tg_id_in_admins:
            raise PermissionError()
        self._validate_item_context(item_id, source, page)
        if action not in ('give', 'take'):
            raise ItemCommandValueError()
        item = await self.logic.item_info(item_id, source=source)
        await self.fsm.clear_this_state()
        await self.fsm.update_data(
            item_id=item_id,
            action=action,
            source=source,
            page=page,
            owned_quantity=owned_quantity,
        )
        await self.fsm.set_state(ItemState.quantity)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.enter_quantity(action, item),
                reply_markup=self.IKB.quantity_cancel(item_id, source, page, owned_quantity),
            )
        ])

    async def change_item_quantity_input(self):
        try:
            quantity = int((self.message.text or '').strip())
        except ValueError:
            raise ItemCommandValueError() from None
        if quantity <= 0:
            raise ItemCommandValueError()

        item_id = await self.fsm.get_value('item_id')
        action = await self.fsm.get_value('action')
        source = await self.fsm.get_value('source')
        page = await self.fsm.get_value('page')
        owned_quantity = await self.fsm.get_value('owned_quantity')
        if (
            not isinstance(item_id, int)
            or action not in ('give', 'take')
            or source not in ('inventory', 'items')
            or not isinstance(page, int)
            or page < 0
        ):
            await self.fsm.set_state()
            raise ItemCommandValueError()
        prompt_message = await self.fsm.get_message()
        if not prompt_message[0] or not prompt_message[1]:
            await self.fsm.set_state()
            await self.fsm.clear_this_state()
            raise ItemCommandStateError()
        self.logic.redact_kwargs(is_admin=True)
        data = await self.logic.change_item(
            action=action,
            item_id=item_id,
            quantity=quantity,
            purpose_tg_id=self.tg_id,
        )
        await self.fsm.set_state()
        await self.fsm.clear_this_state()
        if owned_quantity is not None and source == 'inventory':
            delta = quantity if action == 'give' else -quantity
            owned_quantity = max(0, owned_quantity + delta)
        await self.answer([
            AnswerBody(
                text=self.text.item_changed(data, action, quantity),
                data=data,
                reply_markup=self.IKB.quantity_cancel(
                    item_id=item_id,
                    source=source,
                    page=page,
                    owned_quantity=owned_quantity,
                ),
            )
        ])
        await self.bot.delete_message(*prompt_message)

    async def change_item(
        self,
        action: Literal['give', 'take'],
        item_id: int,
        quantity: int | None = None,
        purpose_tg_id: int | None = None,
    ):
        if not self.is_admin:
            raise PermissionError()
        quantity = 1 if quantity is None else quantity
        if item_id <= 0 or quantity <= 0:
            raise ItemCommandValueError()

        data = await self.logic.change_item(
            action=action,
            item_id=item_id,
            quantity=quantity,
            purpose_tg_id=purpose_tg_id,
        )
        return await self.answer([
            AnswerBody(text=self.text.item_changed(data, action, quantity), data=data)
        ])
