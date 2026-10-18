import uuid
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, User, Update
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from config import settings
from app.logging.base import botlog
from app.aio.cls.msg.utils import TextHTML
from app.aio.cls.callback.base import BaseCall
from app.exception.base import BotError, PythonError, ALienCallbackError
from app.service.base import BaseService

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



class ExceptionMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        dowload = await event.answer('⏳')
        try:
            result = await handler(event, data)
            try:
                await event.delete()
            except Exception:
                pass
            return result
        except BotError as bote:
            botlog.logger.trace(f'AioPartPath: {bote}', tg_id=event.from_user.id, chat_id=event.chat.id)
            await event.answer((TextHTML(bote.to_msg).escape())[:4000])
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            botlog.logger.warning(f'AioPartPath: {e}', tg_id=event.from_user.id, chat_id=event.chat.id)
        except Exception as e:
            str_e = str(e)
            botlog.logger.error(f'AioPartPath: {e}', tg_id=event.from_user.id, chat_id=event.chat.id)
            if event.from_user.id == settings.owner:
                await event.answer(f'{PythonError.msg}: {(TextHTML(str_e).escape())[:4000]}')
            else:
                await event.answer(f'{PythonError.msg}')
            raise e
        finally:
            await dowload.delete()

class ExceptionCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        callback_data: BaseCall = data.get('callback_data', BaseCall(tg_id=0, is_check=True))
        check_is_user = True
        try:
            if check_is_user and callback_data.is_check:
                if event.from_user.id != callback_data.tg_id:
                    raise ALienCallbackError(f'This user enter is alien event keyboard', tg_id=event.from_user.id, chat_id=event.message.chat.id)
            answer_text = ''
            show_alert = None
            result = await handler(event, data)
            return result, event
        except BotError as bote:
            botlog.logger.trace(f'AioPartPath: {bote}', tg_id=event.from_user.id, chat_id=event.message.chat.id)
            show_alert = True
            answer_text = (TextHTML(bote.to_msg).escape())[:4000]
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            botlog.logger.warning(f'AioPartPath: {e}', tg_id=event.from_user.id, chat_id=event.message.chat.id)
        except Exception as e:
            str_e = str(e)
            botlog.logger.error(f'AioPartPath: {e}', tg_id=event.from_user.id, chat_id=event.message.chat.id)
            show_alert = True
            if event.from_user.id == settings.owner:
                answer_text = f'{PythonError.msg}: {(TextHTML(str_e).escape())[:4000]}'
            else:
                answer_text = f'{PythonError.msg}'
            raise e
        finally:
            try:
                await event.answer(answer_text, show_alert=show_alert)
            except Exception as e:
                botlog.logger.error(f'AioPartPath: {e}', tg_id=event.from_user.id, chat_id=event.message.chat.id)
                if event.from_user.id == settings.owner:
                    await event.message.answer(f'⚠️ {(TextHTML(e).escape())[:4000]} \n \n {answer_text}')
                else:
                    await event.answer(f'{PythonError.msg}', show_alert=True)

class ServiceMiddleware(BaseMiddleware):
    def __init__(self, service: type[BaseService]):
        super().__init__()
        self.service = service

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        data['service'] = self.service(user=data.get('event_from_user'), chat=data.get('event_chat'), message=data.get('event_update').message, callback=data.get('event_update').callback_query, state=data.get('state'), request_id=data.get('request_id'))
        return await handler(event, data)
