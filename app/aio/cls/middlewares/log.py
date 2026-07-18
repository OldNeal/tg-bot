from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from app.logging.base import botlog
from datetime import datetime

class BotLogMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        msg = event
        with botlog.logger.contextualize(tg_id=msg.from_user.id, chat_id=msg.chat.id):
            with botlog.logger.catch(reraise=True):
                start = datetime.now()
                result = await handler(event, data)
                end = datetime.now()
                result = f'{int((end - start).total_seconds()*1000)}'
                botlog.message(msg.text, delay=result)
                return result
    