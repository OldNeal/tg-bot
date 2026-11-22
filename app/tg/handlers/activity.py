from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from telegram_click_aio.decorator import command

from app.service.activity import ActivityService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.middlewares import ServiceMiddleware
from app.tg.callback.items import ItemActionCall

activity_router = Router()
activity_router.message.middleware(ServiceMiddleware(ActivityService))
activity_router.callback_query.middleware(ServiceMiddleware(ActivityService))


@activity_router.message(Command('activity_reset'))
@command(
    name='activity_reset',
    description='Сброс лимита очков активности',
    arguments=[Optionals.tg_id, Optionals.is_admin],
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def activity_reset_command(
    message: Message,
    service: ActivityService,
    purpose_tg_id: int | None = None,
    is_admin: bool | None = None,
):
    await service.activity_reset(purpose_tg_id)

@activity_router.callback_query(ItemActionCall.filter(F.action == 'activity_limits'))
async def call(
    callback: CallbackQuery,
    callback_data: ItemActionCall,
    service: ActivityService
):
    await service.limits(
        item_id=callback_data.item_id,
        source=callback_data.source,
        page=callback_data.page
    )


@activity_router.message(F.text, ~F.text.startswith('/'), F.chat.type != 'private')
@flags.is_message_delete(False)
@flags.is_send_dowload_sticker(False)
@flags.is_logging(False)
@flags.is_user_update(False)
async def msg(message: Message, service: ActivityService):
    await service.activity()
