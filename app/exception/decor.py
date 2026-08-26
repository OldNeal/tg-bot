from functools import wraps
from aiogram.types import Message, CallbackQuery
from app.exception.base import BotError, ALienCallbackError, PythonError
from app.logging.base import log
from config import settings
#from app.aio.inline_buttons.faq import FaqIKB
from app.aio.cls.msg.utils import TextHTML
from app.aio.cls.callback.base import BaseCall, MenuCall
import random
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
import traceback
from datetime import datetime

def exept():
    def decor(func):
        @wraps(func)
        async def wrapped(message: Message, **kwargs): 
            dowload = await message.answer('⏳')
            try:
                result = await func(message, **kwargs)
                try:
                    await message.delete()
                except:
                    pass
                return result
            except BotError as bote:
                log.trace(f'AioPartPath: {bote}', tg_id=message.from_user.id, chat_id=message.chat.id)
                #markup = FaqIKB(message.from_user.id).to_error_faq(bote.code) if len(bote.faq) > 0 else None
                await message.answer((TextHTML(bote.to_msg).escape())[:4000])
            except (TelegramBadRequest, TelegramForbiddenError) as e:
                log.warning(f'AioPartPath: {e}', tg_id=message.from_user.id, chat_id=message.chat.id)
            except Exception as e:
                tb = traceback.extract_tb(e.__traceback__)
                for frame in tb:
                    print(f"AioPartPath, Файл: {frame.filename}, строка: {frame.lineno}, функция: {frame.name}")
                    print(f"AioPartPath, Код: {frame.line}\n")
                str_e = str(e)
                log.error(f'AioPartPath: {e}', tg_id=message.from_user.id, chat_id=message.chat.id)
                if message.from_user.id == settings.owner:
                    await message.answer(f'{PythonError.msg}: {(TextHTML(str_e).escape())[:4000]}')
                    await message.answer(f'Файл: {frame.filename}, строка: {frame.lineno}, функция: {frame.name}')
                    await message.answer(f'Код: {frame.line}')
                else:
                    await message.answer(f'{PythonError.msg}')
                raise e
            finally:
                await dowload.delete()
        return wrapped
    return decor

def call_exept(check_is_user: bool = True, tips: list[str] | None = None, rarity_tips: float | None = None):
    def decor(func):
        @wraps(func)
        async def wrapped(callback: CallbackQuery, callback_data: BaseCall, **kwargs): 
            try:
                if check_is_user and callback_data.is_check:
                    if callback.from_user.id != callback_data.tg_id:
                        raise ALienCallbackError(f'This user enter is alien callback keyboard', tg_id=callback.from_user.id, chat_id=callback.message.chat.i)
                answer_text = ''
                show_alert=None
                result = await func(callback, callback_data, **kwargs)
                if tips and rarity_tips:
                    if rarity_tips <= random.random():
                        await callback.answer(random.choice(tips))
                return result, callback
            except BotError as bote:
                log.trace(f'AioPartPath: {bote}', tg_id=callback.from_user.id, chat_id=callback.message.chat.id)
                show_alert=True
                answer_text = (TextHTML(bote.to_msg).escape())[:4000]
            except (TelegramBadRequest, TelegramForbiddenError) as e:
                log.warning(f'AioPartPath: {e}', tg_id=callback.from_user.id, chat_id=callback.message.chat.id)
            except Exception as e:
                str_e = str(e)
                log.error(f'AioPartPath: {e}', tg_id=callback.from_user.id, chat_id=callback.message.chat.id)
                show_alert=True
                if callback.from_user.id == settings.owner:
                    answer_text = f'{PythonError.msg}: {(TextHTML(str_e).escape())[:4000]}'
                else:
                    answer_text = f'{PythonError.msg}'
                raise e
            finally:
                try:
                    await callback.answer(answer_text, show_alert=show_alert)
                except Exception as e:
                    log.error(f'AioPartPath: {e}', tg_id=callback.from_user.id, chat_id=callback.message.chat.id)
                    if callback.from_user.id == settings.owner:
                        await callback.message.answer(f'⚠️ {(TextHTML(e).escape())[:4000]} \n \n {answer_text}')
                    else:
                        await callback.answer(f'{PythonError.msg}', show_alert=True)
    
        return wrapped 
    return decor