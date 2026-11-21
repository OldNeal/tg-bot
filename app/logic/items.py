from typing import Literal

from app.exception.items import ItemUnknownActionError
from app.logic.base import BaseLogic
from app.logic.utils import class_decor


@class_decor
class ItemLogic(BaseLogic):
    async def item_info(self, item_id: int, source: Literal['inventory', 'items'] = 'items'):
        if source == 'inventory':
            return await self.client.item_inventory_info(await self.body, id=item_id)
        return await self.client.item_info(item_id)

    async def inventory(self, page: int | None = None):
        return await self.client.item_inventory(await self.body, page=page)

    async def items(self, page: int | None = None):
        return await self.client.item_list(page=page)

    async def change_item(
        self,
        action: str,
        item_id: int,
        quantity: int,
        purpose_tg_id: int | None = None,
    ):
        purpose_user_id = await self.get_user_id(purpose_tg_id or self.tg_id)
        data = self.schemas.QueryItemChange(
            user_id=await self.user_id,
            is_admin=self.is_admin,
            purpose_user_id=purpose_user_id,
            item_id=item_id,
            quantity=quantity,
        )
        if action == 'give':
            return await self.client.item_give(data)
        if action == 'take':
            return await self.client.item_take(data)
        raise ItemUnknownActionError()
