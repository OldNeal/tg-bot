from telegram_click_aio.decorator import command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandObject

from app.service.main import MainService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.middlewares import ServiceMiddleware
from app.tg.callback.base import MenuCall
from app.tg.callback.main import MainInfoCall, MyStateCall
from app.tg.handlers.beyonder import beyonder_router
from app.tg.handlers.wiki import wiki_router
from app.tg.handlers.organ import organ_router
from app.tg.handlers.stats import stats_router
from app.tg.handlers.news_paper import news_paper_router

main_router = Router()
main_router.message.middleware(ServiceMiddleware(MainService))
main_router.callback_query.middleware(ServiceMiddleware(MainService))
main_router.include_routers(
    beyonder_router,
    organ_router,
    wiki_router,
    stats_router,
    news_paper_router,
)


@main_router.message(Command('menu'))
async def menu(message: Message, service: MainService):
    await service.menu()


@main_router.callback_query(MenuCall.filter(F.where == 'main'))
async def menu_call(callback: CallbackQuery, callback_data: MenuCall, service: MainService):
    await service.menu()


@main_router.callback_query(MenuCall.filter(F.where == 'info'))
async def info_call(callback: CallbackQuery, callback_data: MenuCall, service: MainService):
    await service.info()


@main_router.callback_query(MainInfoCall.filter())
async def main_info_call(callback: CallbackQuery, callback_data: MainInfoCall, service: MainService):
    await service.info(purpose_tg_id=callback_data.purpose_tg_id)


@main_router.message(Command('info'))
@command(
    name='info',
    description='Получить карточку',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: MainService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.info(purpose_tg_id=purpose_tg_id)


@main_router.message(Command('ping'))
@command(
    name='ping',
    description='Проверить соединение',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: MainService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.ping()


@main_router.message(Command('mystate'))
@command(
    name='mystate',
    description='Показать состояние',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: MainService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.my_state()


@main_router.callback_query(MyStateCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: MyStateCall,
    service: MainService
):
    await service.my_state()


@main_router.message(Command('mystateclear'))
@command(
    name='mystateclear',
    description='Очистить состояние',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: MainService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.my_state_clear()


@main_router.message(Command('mystatepop'))
@command(
    name='mystatepop',
    description='Удалить значение состояния',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: MainService,
    command: CommandObject,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.my_state_pop(command)
