from datetime import datetime, timedelta

from telegram_click_aio.decorator import command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from app.service.beyonder import BeyonderService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Requireds, Optionals
from app.tg.callback.beyonder import DrinkCall, KillCall, BeyonderListCall, BeyonderListPageCall, BeyonderInfoCall, BeyonderBackCall
from app.tg.callback.back_values import BeyonderBackValues
from app.tg.middlewares import ServiceMiddleware

beyonder_router = Router()
beyonder_router.message.middleware(ServiceMiddleware(BeyonderService))
beyonder_router.callback_query.middleware(ServiceMiddleware(BeyonderService))


@beyonder_router.message(Command('beyonder'))
@command(
    name='beyonder',
    arguments=[
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    description='Карточка потустороннего',
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.info(purpose_tg_id)


@beyonder_router.callback_query(BeyonderInfoCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: BeyonderInfoCall,
    service: BeyonderService
):
    await service.info(callback_data.purpose_tg_id)


@beyonder_router.message(Command('drink'))
@command(
    name='drink',
    description='Выпить зелье',
    arguments=[
        Optionals.path_name,
        Optionals.drink_seq,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    path_name: str | None = None,
    seq: int = 9,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.drink(path_name=path_name, seq=seq, purpose_tg_id=purpose_tg_id)


@beyonder_router.callback_query(DrinkCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: DrinkCall,
    service: BeyonderService
):
    await service.drink(path_id=callback_data.path_id)


@beyonder_router.message(Command('upseq'))
@command(
    name='upseq',
    description='Поднять последовательонсть',
    arguments=[
        Optionals.seq,
        Optionals.path_name,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    seq: int | None = None,
    path_name: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.upseq(seq=seq, path_name=path_name, purpose_tg_id=purpose_tg_id)


@beyonder_router.message(Command('downseq'))
@command(
    name='downseq',
    description='Понизить последовательонсть',
    arguments=[
        Optionals.seq,
        Optionals.path_name,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    seq: int | None = None,
    path_name: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.dowseq(seq=seq, path_name=path_name, purpose_tg_id=purpose_tg_id)


@beyonder_router.message(Command('kill'))
@command(
    name='kill',
    description='Потерять контроль',
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
    service: BeyonderService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.kill(purpose_tg_id=purpose_tg_id, is_admin=is_admin)


@beyonder_router.callback_query(KillCall.filter(F.accert == True))
async def call(
    callback: CallbackQuery,
    callback_data: KillCall,
    service: BeyonderService
):
    await service.accert_kill(callback_data.purpose_tg_id)


@beyonder_router.callback_query(KillCall.filter(F.cancel == True))
async def call(
    callback: CallbackQuery,
    callback_data: KillCall,
    service: BeyonderService
):
    await service.cancel_kill(callback_data.purpose_tg_id)


@beyonder_router.message(Command('time'), F.text.contains('redact'))
@command(
    name='time redact',
    description='Изменить время продвижения',
    arguments=[
        Requireds.time_mode,
        Requireds.duration,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    time_mode: str,
    duration: timedelta,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.time_redact(duration=duration, purpose_tg_id=purpose_tg_id)


@beyonder_router.message(Command('time'), F.text.contains('replace'))
@command(
    name='time replace',
    description='Заменить время продвижения',
    arguments=[
        Requireds.time_mode,
        Requireds.date,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    time_mode: str,
    datetime_arg: datetime,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.time_replace(datetime_arg=datetime_arg, purpose_tg_id=purpose_tg_id)


@beyonder_router.message(Command('time'), F.text.contains('info'))
@command(
    name='time info',
    description='Узнать информацию о продвижении',
    arguments=[
        Optionals.time_mode,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: BeyonderService,
    time_mode: str = 'info',
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.time_info(purpose_tg_id=purpose_tg_id)


@beyonder_router.message(Command('time'))
@command(
    name='time',
    description='Узнать информацию о продвижении',
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
    service: BeyonderService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.time_info(purpose_tg_id=purpose_tg_id)


@beyonder_router.callback_query(BeyonderListCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: BeyonderListCall,
    service: BeyonderService
):
    await service.list(callback_data.path_id)


@beyonder_router.callback_query(BeyonderListPageCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: BeyonderListPageCall,
    service: BeyonderService
):
    await service.list(callback_data.path_id, callback_data.page, where=callback_data.where)


@beyonder_router.callback_query(BeyonderBackCall.filter(F.where == BeyonderBackValues.list))
async def call(
    callback: CallbackQuery,
    callback_data: BeyonderBackCall,
    service: BeyonderService
):
    await service.list()
