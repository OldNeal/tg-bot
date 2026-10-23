from telegram_click_aio.decorator import command
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

from app.service.help import HelpService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.middlewares import ServiceMiddleware

help_router = Router()
help_router.message.middleware(ServiceMiddleware(HelpService))
help_router.callback_query.middleware(ServiceMiddleware(HelpService))


@help_router.message(Command('help'))
@command(
    name='help',
    description='Получить список команд',
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
    service: HelpService,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
    is_admin: bool = False,
):
    await service.main()
