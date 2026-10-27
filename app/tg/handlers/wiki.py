from telegram_click_aio.decorator import command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from app.service.wiki import WikiService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.callback.base import MenuCall
from app.tg.callback.wiki import (
    PathCall,
    GroupCall,
    WikiBackCall,
    GACall,
    WikiMenuCall,
    WikiSearchCall,
    PathsPageCall,
    GasPageCall,
)
from app.tg.callback.back_values import WikiBackValues
from app.tg.fsm.state import WikiState
from app.tg.middlewares import ServiceMiddleware

wiki_router = Router()
wiki_router.message.middleware(ServiceMiddleware(WikiService))
wiki_router.callback_query.middleware(ServiceMiddleware(WikiService))


@wiki_router.callback_query(MenuCall.filter(F.where == 'wiki'))
async def main_menu_call(callback: CallbackQuery, callback_data: MenuCall, service: WikiService):
    await service.menu()


@wiki_router.message(Command('wiki'))
@command(
    name='wiki',
    description='Вызвать вики-меню',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: WikiService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.menu()


@wiki_router.callback_query(WikiMenuCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: WikiMenuCall,
    service: WikiService,
):
    await service.menu(callback_data.type)


@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.menu))
async def call(
    callback: CallbackQuery,
    callback_data: WikiBackCall,
    service: WikiService,
):
    await service.menu()


@wiki_router.message(Command('ga'))
@command(
    name='ga',
    description='Получить информацию о великих древних',
    arguments=[
        Optionals.value,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: WikiService,
    value: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.ga(value)


@wiki_router.callback_query(GroupCall.filter(F.type == 'ga'))
async def call(
    callback: CallbackQuery,
    callback_data: GroupCall,
    service: WikiService,
):
    await service.all_gas(callback_data.name)


@wiki_router.callback_query(GACall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: GACall,
    service: WikiService,
):
    await service.get_ga(id=callback_data.id)


@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.gas))
async def call(
    callback: CallbackQuery,
    callback_data: WikiBackCall,
    service: WikiService,
):
    await service.back_ga(callback_data.is_all)


@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.ga))
async def call(
    callback: CallbackQuery,
    callback_data: WikiBackCall,
    service: WikiService,
):
    await service.get_ga()


@wiki_router.message(Command('path'))
@command(
    name='path',
    description='Получить информацию о путях',
    arguments=[
        Optionals.value,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: WikiService,
    value: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.path(value)


@wiki_router.callback_query(GroupCall.filter(F.type == 'path'))
async def call(
    callback: CallbackQuery,
    callback_data: GroupCall,
    service: WikiService,
):
    await service.all_paths(callback_data.name)


@wiki_router.callback_query(PathCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: PathCall,
    service: WikiService,
):
    await service.get_path(id=callback_data.id)


@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.search))
@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.paths))
async def call(
    callback: CallbackQuery,
    callback_data: WikiBackCall,
    service: WikiService,
):
    await service.back_path(callback_data.is_all)


@wiki_router.callback_query(WikiSearchCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: WikiSearchCall,
    service: WikiService,
):
    await service.to_enter_search_value(callback_data.type)


@wiki_router.message(WikiState.search)
async def text_state(message: Message, service: WikiService):
    await service.enter_search_value()


@wiki_router.callback_query(PathsPageCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: PathsPageCall,
    service: WikiService,
):
    await service.search_path(value=callback_data.value, page=callback_data.page)


@wiki_router.callback_query(GasPageCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: GasPageCall,
    service: WikiService,
):
    await service.search_ga(value=callback_data.value, page=callback_data.page)
