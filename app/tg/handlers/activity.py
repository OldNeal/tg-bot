from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from telegram_click_aio.decorator import command

from app.service.activity import ActivityService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.middlewares import ServiceMiddleware

activity_router = Router()
activity_router.message.middleware(ServiceMiddleware(ActivityService))


@activity_router.message(Command('activity_reset'))
@command(
    name='activity_reset',
    description='Сброс лимита очков активности',
    arguments=[Optionals.tg_id],
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def activity_reset_command(
    message: Message,
    service: ActivityService,
    purpose_tg_id: int | None = None,
):
    await service.activity_reset(purpose_tg_id)


@activity_router.message(F.text, ~F.text.startswith('/'), F.chat.type != 'private')
@flags.is_message_delete(False)
@flags.is_send_dowload_sticker(False)
@flags.is_logging(False)
async def msg(message: Message, service: ActivityService):
    await service.activity()
