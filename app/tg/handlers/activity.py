from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from telegram_click_aio.decorator import command

from app.service.activity import ActivityService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals, Requireds
from app.tg.middlewares import ServiceMiddleware

activity_router = Router()
activity_router.message.middleware(ServiceMiddleware(ActivityService))


@activity_router.message(Command('ap'))
@command(
    name='ap',
    description='Очки активности: просмотр и управление',
    arguments=[
        Requireds.activity_action,
        Optionals.tg_id,
        Optionals.activity_points,
        Optionals.activity_reason,
        Optionals.to_json,
        Optionals.is_reply,
        Optionals.is_admin,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def ap_command(
    message: Message,
    service: ActivityService,
    action: str,
    purpose_tg_id: int | None = None,
    points: int | None = None,
    reason: str | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.ap(action, purpose_tg_id, points, reason)


@activity_router.message(F.text, ~F.text.startswith('/'), F.chat.type != 'private')
@flags.is_message_delete(False)
@flags.is_send_dowload_sticker(False)
@flags.is_logging(False)
async def msg(message: Message, service: ActivityService):
    await service.activity()
