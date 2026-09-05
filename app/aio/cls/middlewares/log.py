from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from app.logging.base import botlog
from datetime import datetime
import uuid

class BotLogMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        msg = event
        request_id = uuid.uuid4().hex
        is_delay = any([p+d in msg.text for d in ['delay', 'is_delay', 'd'] for p in ['--', '-', '—']])
        with botlog.logger.contextualize(tg_id=msg.from_user.id, chat_id=msg.chat.id, request_id=request_id):
            if not is_delay:
                botlog.message(msg.text)
            with botlog.logger.catch(reraise=True):
                start = datetime.now()
                data['request_id'] = request_id
                result = await handler(event, data)
                end = datetime.now()
                if is_delay:
                    result = f'{int((end - start).total_seconds()*1000)}'
                    botlog.message(msg.text, delay=result)
                return result
            
class BotLogCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        callback = event
        request_id = uuid.uuid4().hex
        is_delay = False
        with botlog.logger.contextualize(tg_id=callback.from_user.id, chat_id=callback.message.chat.id, request_id=request_id):
            if not is_delay:
                botlog.callback(callback.data)
            with botlog.logger.catch(reraise=True):
                start = datetime.now()
                data['request_id'] = request_id
                result = await handler(event, data)
                end = datetime.now()
                if is_delay:
                    result = f'{int((end - start).total_seconds()*1000)}'
                return result
    