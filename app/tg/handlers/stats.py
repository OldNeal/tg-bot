from telegram_click_aio.decorator import command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from app.service.stats import StatsService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.callback.stats import StatsBackCall, BackCall, StatsPageCall, StatsPathsCall
from app.tg.callback.back_values import StatsBackValues
from app.tg.fsm.state import StatsState
from app.tg.middlewares import ServiceMiddleware

stats_router = Router()
stats_router.message.middleware(ServiceMiddleware(StatsService))
stats_router.callback_query.middleware(ServiceMiddleware(StatsService))


@stats_router.message(Command('stats'))
@command(
    name='stats',
    description='Получить статистику',
    arguments=[
        Optionals.value,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def cmd(
    message: Message,
    service: StatsService,
    value: str | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False
):
    await service.all(value=value)


@stats_router.callback_query(StatsBackCall.filter(F.where == StatsBackValues.all))
async def call(
    callback: CallbackQuery,
    callback_data: StatsBackCall,
    service: StatsService
):
    await service.all()


@stats_router.callback_query(StatsPathsCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: StatsPathsCall,
    service: StatsService
):
    await service.back_paths()


@stats_router.callback_query(StatsBackCall.filter(F.where == StatsBackValues.stats_paths))
@stats_router.callback_query(BackCall.filter(F.where == StatsBackValues.stats_paths))
async def call(
    callback: CallbackQuery,
    callback_data: BackCall,
    service: StatsService
):
    await service.paths()


@stats_router.callback_query(StatsPageCall.filter())
async def call(
    callback: CallbackQuery,
    callback_data: StatsPageCall,
    service: StatsService
):
    await service.paths(value=callback_data.value, page=callback_data.page)


@stats_router.message(StatsState.search)
async def text_state(
    message: Message,
    service: StatsService
):
    await service.enter_path()
