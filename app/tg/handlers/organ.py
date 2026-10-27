from telegram_click_aio.decorator import command
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.tg.args import Optionals, Requireds
from app.tg.callback.base import MenuCall
from app.tg.callback.back_values import OrganBackValues
from app.tg.callback.organ import (
    OrganBackCall,
    OrganCaptureCall,
    OrganCreateCall,
    OrganExitCall,
    OrganGiveCall,
    OrganInfoCall,
    OrganInfoDescCall,
    OrganInfoMembersCall,
    OrganKickCall,
    OrganLoginCall,
    OrganMemberCall,
    OrganMemberPageCall,
    OrganMyCall,
    OrganPageCall,
    OrganRankRedactCall,
    OrganSearchCall,
    OrganSettingCall,
    OrganSettingParametrDefaultCall,
    OrganSettingRedactCall,
    OrganTitulDeleteCall,
    OrganTitulRedactCall,
)
from app.tg.fsm.state import OrganState
from app.tg.middlewares import ServiceMiddleware
from app.service.organ import OrganService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER

organ_router = Router()
organ_router.message.middleware(ServiceMiddleware(OrganService))
organ_router.callback_query.middleware(ServiceMiddleware(OrganService))


@organ_router.callback_query(MenuCall.filter(F.where == 'organ'))
async def menu_call(callback: CallbackQuery, callback_data: MenuCall, service: OrganService):
    await service.menu()


@organ_router.message(Command('member'))
@command(
    name='member',
    description='Информация о участнике',
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
    service: OrganService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.member(purpose_tg_id=purpose_tg_id)


@organ_router.message(Command('organ'), F.text.contains('member'), F.text.not_contains('members'))
@command(
    name='organ member',
    description='Информация о участнике',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.member(purpose_tg_id=purpose_tg_id)


@organ_router.callback_query(OrganMemberCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganMemberCall,
    service: OrganService,
):
    await service.member(purpose_tg_id=callback_data.purpose_tg_id)


@organ_router.message(Command('organ'), F.text.contains('search'))
@command(
    name='organ search',
    description='Найти организацию',
    arguments=[
        Requireds.organ_mode,
        Optionals.organ_value,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    value: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.search(value=value)


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.search))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.search()


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.menu))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.menu()


@organ_router.callback_query(OrganSearchCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganSearchCall,
    service: OrganService,
):
    await service.search(is_new_search=True)


@organ_router.message(OrganState.search)
async def text_state(
    message: Message,
    state: FSMContext,
    service: OrganService,
):
    msg0 = await service.fsm.get_message()
    await service.to_search()
    await service.fsm.set_state()
    await service.bot.delete_message(*msg0)
    await service.fsm.remove_message()


@organ_router.callback_query(OrganPageCall.filter(F.is_search == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganPageCall,
    service: OrganService,
):
    await service.search(page=callback_data.page)


@organ_router.message(Command('organ'), F.text.contains('info'))
@command(
    name='organ info',
    description='Информация о организации',
    arguments=[
        Requireds.organ_mode,
        Optionals.organ_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    organ_id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.info(organ_id=organ_id, purpose_tg_id=purpose_tg_id)


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.info))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.info(is_back=True)


@organ_router.callback_query(OrganInfoCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganInfoCall,
    service: OrganService,
):
    await service.info(
        organ_id=callback_data.organ_id,
        purpose_tg_id=callback_data.purpose_tg_id,
    )


@organ_router.message(Command('organ'), F.text.contains('members'))
@command(
    name='organ members',
    description='Участники организации',
    arguments=[
        Requireds.organ_mode,
        Optionals.organ_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    organ_id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.info_members(organ_id=organ_id)


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.members))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.info(is_back=True)


@organ_router.callback_query(OrganInfoMembersCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganInfoMembersCall,
    service: OrganService,
):
    await service.info_members(organ_id=callback_data.organ_id)


@organ_router.callback_query(OrganMemberPageCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganMemberPageCall,
    service: OrganService,
):
    await service.info_members(
        organ_id=callback_data.organ_id,
        page=callback_data.page,
    )


@organ_router.message(
    Command('organ'),
    F.text.contains('description') | F.text.contains('desc'),
)
@command(
    name='organ description',
    description='Описание организации',
    arguments=[
        Requireds.organ_mode,
        Optionals.organ_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    organ_id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.info_description(organ_id=organ_id)


@organ_router.callback_query(OrganInfoDescCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganInfoDescCall,
    service: OrganService,
):
    await service.info_description(organ_id=callback_data.organ_id)


@organ_router.message(Command('organ'), F.text.contains('list'))
@command(
    name='organ list',
    description='Организации',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.list()


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.list))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.list()


@organ_router.callback_query(OrganPageCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganPageCall,
    service: OrganService,
):
    await service.list(page=callback_data.page)


@organ_router.message(Command('organ'), F.text.contains('top'))
@command(
    name='organ top',
    description='Топ организаций',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.top()


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.top))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.top()


@organ_router.message(Command('login'))
@command(
    name='login',
    description='Войти в организацию',
    arguments=[
        Optionals.organ_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.login(organ_id=organ_id)


@organ_router.message(Command('organ'), F.text.contains('login'))
@command(
    name='organ login',
    description='Войти в организацию',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.login()


@organ_router.callback_query(OrganLoginCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganLoginCall,
    service: OrganService,
):
    await service.login(organ_id=callback_data.organ_id)


@organ_router.message(Command('exit'))
@command(
    name='exit',
    description='Выйти из организации',
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
    service: OrganService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.to_exit()


@organ_router.message(Command('organ'), F.text.contains('exit'))
@command(
    name='organ exit',
    description='Выйти из организации',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.to_exit()


@organ_router.callback_query(OrganExitCall.filter(F.accert == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganExitCall,
    service: OrganService,
):
    await service.exit()


@organ_router.callback_query(OrganExitCall.filter(F.cancel == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganExitCall,
    service: OrganService,
):
    await service.cancel_exit()


@organ_router.callback_query(OrganExitCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganExitCall,
    service: OrganService,
):
    await service.to_exit()


@organ_router.message(
    Command('organ'),
    F.text.contains('create') | F.text.contains('new'),
)
@command(
    name='organ create',
    description='Создать организацию',
    arguments=[Requireds.organ_mode, Optionals.organ_name],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    name: str | None = None,
):
    await service.create(name=name)


@organ_router.callback_query(OrganCreateCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganCreateCall,
    service: OrganService,
):
    await service.to_enter_name_for_create()


@organ_router.message(OrganState.create)
async def text_state(
    message: Message,
    state: FSMContext,
    service: OrganService,
):
    msg0 = await service.fsm.get_message()
    await service.enter_name_for_create()
    await service.fsm.set_state()
    await service.bot.delete_message(*msg0)
    await service.fsm.remove_message()


@organ_router.message(
    Command('organ'),
    F.text.contains('setting') | F.text.contains('settings'),
)
@command(
    name='organ setting',
    description='Настройки организации',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.get_settings()


@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.settings))
async def call(
    callback: CallbackQuery,
    callback_data: OrganBackCall,
    service: OrganService,
):
    await service.get_settings()


@organ_router.callback_query(OrganSettingCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganSettingCall,
    service: OrganService,
):
    await service.get_settings()


@organ_router.callback_query(OrganSettingRedactCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganSettingRedactCall,
    service: OrganService,
):
    await service.to_redact_settings()


@organ_router.callback_query(OrganSettingParametrDefaultCall.filter(F.is_all == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganSettingParametrDefaultCall,
    service: OrganService,
):
    await service.default_settings()


@organ_router.message(OrganState.settings)
async def text_state(
    message: Message,
    state: FSMContext,
    service: OrganService,
):
    msg0 = await service.fsm.get_message()
    await service.redact_settings()
    await service.fsm.set_state()
    await service.bot.delete_message(*msg0)
    await service.fsm.remove_message()


@organ_router.message(Command('organ'), F.text.contains('capture'))
@command(
    name='organ capture',
    description='Захватить организациб',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.capture()


@organ_router.callback_query(OrganCaptureCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganCaptureCall,
    service: OrganService,
):
    await service.capture()


@organ_router.message(Command('uprank'))
@command(
    name='uprank',
    description='Повысить ранг участника',
    arguments=[
        Optionals.rank,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    rank: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.uprank(purpose_tg_id=purpose_tg_id, rank=rank)


@organ_router.message(Command('organ'), F.text.contains('uprank'))
@command(
    name='organ uprank',
    description='Повысить ранг участника',
    arguments=[
        Requireds.organ_mode,
        Optionals.rank,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    rank: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.uprank(purpose_tg_id=purpose_tg_id, rank=rank)


@organ_router.message(Command('downrank'))
@command(
    name='downrank',
    description='Понизить ранг участника',
    arguments=[
        Optionals.rank,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    rank: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.downrank(purpose_tg_id=purpose_tg_id, rank=rank)


@organ_router.message(Command('organ'), F.text.contains('downrank'))
@command(
    name='organ downrank',
    description='Понизить ранг участника',
    arguments=[
        Requireds.organ_mode,
        Optionals.rank,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    rank: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.downrank(purpose_tg_id=purpose_tg_id, rank=rank)


@organ_router.callback_query(OrganRankRedactCall.filter(F.operation == 'up'))
async def call(
    callback: CallbackQuery,
    callback_data: OrganRankRedactCall,
    service: OrganService,
):
    await service.uprank(purpose_tg_id=callback_data.purpose_tg_id)


@organ_router.callback_query(OrganRankRedactCall.filter(F.operation == 'down'))
async def call(
    callback: CallbackQuery,
    callback_data: OrganRankRedactCall,
    service: OrganService,
):
    await service.downrank(purpose_tg_id=callback_data.purpose_tg_id)


@organ_router.message(Command('organ'), F.text.contains('kick'))
@command(
    name='organ kick',
    description='Выгнать участника',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.kick(purpose_tg_id=purpose_tg_id)


@organ_router.callback_query(OrganKickCall.filter(F.accert == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganKickCall,
    service: OrganService,
):
    await service.accert_kick(callback_data.purpose_tg_id)


@organ_router.callback_query(OrganKickCall.filter(F.cancel == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganKickCall,
    service: OrganService,
):
    await service.cancel_kick()


@organ_router.callback_query(OrganKickCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganKickCall,
    service: OrganService,
):
    await service.kick(callback_data.purpose_tg_id)


@organ_router.message(
    Command('titul'),
    F.text.contains('delete') | F.text.contains('del'),
)
@command(
    name='titul delete',
    description='Убрать титул участника',
    arguments=[
        Requireds.titul_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    titul_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.titul_delete(purpose_tg_id=purpose_tg_id)


@organ_router.message(
    Command('organ'),
    F.text.contains('titul delete') | F.text.contains('titul del'),
)
@command(
    name='organ titul delete',
    description='Убрать титул участника',
    arguments=[
        Requireds.organ_mode,
        Requireds.titul_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    titul_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.titul_delete(purpose_tg_id=purpose_tg_id)


@organ_router.callback_query(OrganTitulDeleteCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganTitulDeleteCall,
    service: OrganService,
):
    await service.titul_delete(callback_data.purpose_tg_id)


@organ_router.message(Command('titul'), F.text.contains('redact'))
@command(
    name='titul redact',
    description='Поменять титул участника',
    arguments=[
        Requireds.titul_mode,
        Optionals.titul,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    titul_mode: str,
    titul: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.titul(purpose_tg_id=purpose_tg_id, titul=titul)


@organ_router.message(Command('organ'), F.text.contains('titul redact'))
@command(
    name='organ titul redact',
    description='Редактировать титул участника',
    arguments=[
        Requireds.organ_mode,
        Requireds.titul_mode,
        Optionals.titul,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    titul_mode: str,
    titul: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.titul(purpose_tg_id=purpose_tg_id, titul=titul)


@organ_router.callback_query(OrganTitulRedactCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganTitulRedactCall,
    service: OrganService,
):
    await service.titul(purpose_tg_id=callback_data.purpose_tg_id)


@organ_router.message(OrganState.titul)
async def text_state(
    message: Message,
    state: FSMContext,
    service: OrganService,
):
    msg0 = await service.fsm.get_message()
    await service.titul_redact()
    await service.fsm.set_state()
    await service.bot.delete_message(*msg0)
    await service.fsm.remove_message()


@organ_router.message(Command('titul'))
@command(
    name='titul',
    description='Редактировать титул участника',
    arguments=[
        Optionals.titul,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    titul: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.titul(purpose_tg_id=purpose_tg_id, titul=titul)


@organ_router.message(Command('organ'), F.text.contains('titul'))
@command(
    name='organ titul',
    description='Редактировать титул участника',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.titul(purpose_tg_id=purpose_tg_id)


@organ_router.message(Command('organ'), F.text.contains('give'))
@command(
    name='organ give',
    description='Передать организацию',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.to_give(purpose_tg_id=purpose_tg_id)


@organ_router.callback_query(OrganGiveCall.filter(F.accert == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganGiveCall,
    service: OrganService,
):
    await service.give(callback_data.purpose_tg_id)


@organ_router.callback_query(OrganGiveCall.filter(F.cancel == True))
async def call(
    callback: CallbackQuery,
    callback_data: OrganGiveCall,
    service: OrganService,
):
    await service.cancel_give()


@organ_router.callback_query(OrganGiveCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganGiveCall,
    service: OrganService,
):
    await service.to_give(callback_data.purpose_tg_id)


@organ_router.message(Command('organ'), F.text.contains('menu'))
@command(
    name='organ menu',
    description='Передать организацию',
    arguments=[
        Requireds.organ_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_mode: str,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.menu()


@organ_router.message(Command('organ'))
@command(
    name='organ',
    description='Меню организации',
    arguments=[
        Optionals.organ_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: OrganService,
    organ_id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.menu()


@organ_router.callback_query(OrganMyCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: OrganMyCall,
    service: OrganService,
):
    await service.my_organ()
