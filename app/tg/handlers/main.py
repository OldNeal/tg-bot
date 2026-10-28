from telegram_click_aio.decorator import command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from app.service.main import MainService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals, Requireds
from app.tg.middlewares import ServiceMiddleware
from app.tg.callback.base import MenuCall
from app.tg.callback.main import (
    MainInfoCall,
    MainUserInfoCall,
    MainUserDeleteCall,
    MainUsersCall,
    MainUsersPageCall,
    MainUsersSearchCall,
    MainUsersSearchFieldCall,
    MyStateCall,
)
from app.tg.fsm.state import MainState
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

@main_router.message(Command('user'))
@command(
    name='user',
    description='Список и поиск пользователей',
    arguments=[
        Optionals.user_id, 
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
        ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def users_command(
    message: Message,
    service: MainService,
    user_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.user_info(user_id)


@main_router.message(Command('users'))
@command(
    name='users',
    description='Список и поиск пользователей',
    arguments=[Optionals.is_admin],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def users_command(
    message: Message,
    service: MainService,
    is_admin: bool = False,
):
    await service.users()


@main_router.message(Command('deleteuser'))
@command(
    name='deleteuser',
    description='Запросить подтверждение удаления аккаунта',
    arguments=[Optionals.user_id, Optionals.is_admin],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def delete_user_command(
    message: Message,
    service: MainService,
    user_id: int | None = None,
    is_admin: bool = False,
):
    await service.confirm_user_delete(user_id)


@main_router.callback_query(MainUsersCall.filter())
async def users_list_call(
    callback: CallbackQuery,
    callback_data: MainUsersCall,
    service: MainService,
):
    await service.users()


@main_router.callback_query(MainUsersSearchCall.filter())
async def users_search_call(
    callback: CallbackQuery,
    callback_data: MainUsersSearchCall,
    service: MainService,
):
    await service.users_search_fields()


@main_router.callback_query(MainUsersSearchFieldCall.filter())
async def users_search_field_call(
    callback: CallbackQuery,
    callback_data: MainUsersSearchFieldCall,
    service: MainService,
):
    await service.to_users_search(callback_data.field)


@main_router.callback_query(MainUsersPageCall.filter())
async def users_page_call(
    callback: CallbackQuery,
    callback_data: MainUsersPageCall,
    service: MainService,
):
    await service.users_page(callback_data.page)


@main_router.message(MainState.users_search)
async def users_search_text(
    message: Message,
    state: FSMContext,
    service: MainService,
):
    await service.search_users()


@main_router.callback_query(MainUserDeleteCall.filter())
async def user_delete_call(
    callback: CallbackQuery,
    callback_data: MainUserDeleteCall,
    service: MainService,
):
    if callback_data.confirmed is None:
        await service.confirm_user_delete(callback_data.user_id)
    elif callback_data.confirmed:
        await service.delete_user(callback_data.user_id, confirmed=True)
    else:
        await service.delete_user(callback_data.user_id, confirmed=False)


@main_router.callback_query(MainUserInfoCall.filter())
async def user_info_call(
    callback: CallbackQuery,
    callback_data: MainUserInfoCall,
    service: MainService,
):
    await service.user_info(callback_data.user_id)


@main_router.callback_query(MenuCall.filter(F.where == 'main'))
async def menu_call(callback: CallbackQuery, callback_data: MenuCall, service: MainService):
    await service.menu()


@main_router.callback_query(MenuCall.filter(F.where == 'info'))
async def info_call(callback: CallbackQuery, callback_data: MenuCall, service: MainService):
    await service.info()

@main_router.callback_query(MenuCall.filter(F.where == 'user'))
async def user_call(callback: CallbackQuery, callback_data: MenuCall, service: MainService):
    await service.user_info()

@main_router.callback_query(MenuCall.filter(F.where == 'users'))
async def users_call(callback: CallbackQuery, callback_data: MenuCall, service: MainService):
    await service.users()

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
