from typing import Literal

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from telegram_click_aio.decorator import command

from app.service.items import ItemService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals, Requireds
from app.tg.callback.base import MenuCall
from app.tg.callback.items import (
    ItemInfoCall,
    ItemInventoryCall,
    ItemInventoryPageCall,
    ItemQuantityCall,
    ItemsPageCall,
)
from app.tg.fsm.state import ItemState
from app.tg.middlewares import ServiceMiddleware

items_router = Router()
items_router.message.middleware(ServiceMiddleware(ItemService))
items_router.callback_query.middleware(ServiceMiddleware(ItemService))


@items_router.message(Command('inventory'))
@command(
    name='inventory',
    description='Посмотреть свой инвентарь',
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def inventory_command(message: Message, service: ItemService):
    await service.inventory()


@items_router.message(Command('items'))
@command(
    name='items',
    description='Список предметов',
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def items_command(message: Message, service: ItemService):
    await service.items()


@items_router.message(Command('item'))
@command(
    name='item',
    description='Выдать или забрать предмет (для администраторов)',
    arguments=[
        Requireds.item_action,
        Requireds.item_id,
        Optionals.item_quantity,
        Optionals.tg_id,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def change_item_command(
    message: Message,
    service: ItemService,
    action: Literal['give', 'take'],
    item_id: int,
    quantity: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.change_item(
        action=action,
        item_id=item_id,
        quantity=quantity,
        purpose_tg_id=purpose_tg_id,
    )


@items_router.callback_query(ItemInventoryCall.filter())
async def inventory_call(
    callback: CallbackQuery,
    callback_data: ItemInventoryCall,
    service: ItemService,
):
    await service.inventory()


@items_router.callback_query(ItemInventoryPageCall.filter())
async def inventory_page_call(
    callback: CallbackQuery,
    callback_data: ItemInventoryPageCall,
    service: ItemService,
):
    await service.inventory(page=callback_data.page)


@items_router.callback_query(ItemsPageCall.filter())
async def items_page_call(
    callback: CallbackQuery,
    callback_data: ItemsPageCall,
    service: ItemService,
):
    await service.items(page=callback_data.page)


@items_router.callback_query(ItemInfoCall.filter())
async def item_info_call(
    callback: CallbackQuery,
    callback_data: ItemInfoCall,
    service: ItemService,
):
    await service.item_info(
        item_id=callback_data.item_id,
        source=callback_data.source,
        page=callback_data.page,
        owned_quantity=callback_data.owned_quantity,
    )


@items_router.callback_query(ItemQuantityCall.filter())
async def item_quantity_call(
    callback: CallbackQuery,
    callback_data: ItemQuantityCall,
    service: ItemService,
):
    await service.start_quantity_input(
        item_id=callback_data.item_id,
        action=callback_data.action,
        source=callback_data.source,
        page=callback_data.page,
        owned_quantity=callback_data.owned_quantity,
    )


@items_router.message(ItemState.quantity)
async def item_quantity_input(
    message: Message,
    state: FSMContext,
    service: ItemService,
):
    await service.change_item_quantity_input()


@items_router.callback_query(MenuCall.filter(F.where == 'items'))
async def items_menu_call(
    callback: CallbackQuery,
    callback_data: MenuCall,
    service: ItemService,
):
    await service.items()
