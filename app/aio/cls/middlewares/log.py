from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.logging.base import botlog

class BotLogMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        msg = event
        with botlog.logger.contextualize(tg_id=msg.from_user.id, chat_id=msg.chat.id):
            botlog.message(msg.text)
            with botlog.logger.catch(reraise=True):
                result = await handler(event, data)
                return result
    