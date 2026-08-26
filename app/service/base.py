import asyncio, functools
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputRichMessage
from aiogram.filters import CommandStart, Command, CommandObject
from app.aio.cls.buttons.base import BotIKB
from config import settings, bot, log, botlog
from app.aio.cls.fsm.utils import FSMUtils
from app.service.utils import is_natural_int
from app.validate.service import Purpose
from app.validate.base import BaseValidate, BaseModel
from app.aio.cls.msg.utils import TextHTML
from typing import TypeVar

NOT_NEW_STATE = object()
DATA_PAGE = TypeVar('DATA_PAGE')

class BaseService:
    def __init__(self, 
                 message: Message, 
                 state: FSMContext | None = None, 
                 callback: CallbackQuery | None = None, 
                 command: CommandObject | None = None, 
                 logic_kwargs: dict = {}, 
                 **kwargs):
        self.settings = settings
        self.bot = bot
        self.message = message
        self.callback = callback
        self.command = command
        self.kwargs = kwargs
        self.user = self.callback.from_user if self.callback else self.message.from_user
        self.tg_id = self.user.id
        self.logic_kwargs = {'is_admin':self.is_admin} | logic_kwargs

        self.is_bot_message = bool(self.callback)
        self.state: FSMUtils = FSMUtils(state)
        self.IKB = BotIKB(self.tg_id)
        self.text = None
        self.logic = None
        self.asyncio = asyncio
        self.datetime = datetime
        self.log = log
        self.botlog = botlog
        self.msg_to_json: bool = self.kwargs.get('to_json', False)
        self.enter_args: bool = self.command.args != None if command else False


    @property
    def purpose(self):
        if self.message.is_topic_message and self.kwargs.get('is_reply') and self.message.reply_to_message:
            return self.message.reply_to_message.from_user
        elif self.message.reply_to_message:
            return self.message.reply_to_message.from_user
        else:
            return self.user

    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False) and self.tg_id in self.settings.admins

    @classmethod
    def is_natural_int(self, value, **kwargs):
        return is_natural_int(value, **kwargs)

    async def get_news_channel_info(self):
        channel = await self.bot.get_chat(self.settings.news_group_id)
        return channel
    
    async def get_chat_member(self, tg_id: int | None = None):
        if tg_id:
            return await bot.get_chat_member(self.settings.news_group_id, tg_id)
        return await bot.get_chat_member(self.settings.news_group_id, self.tg_id)

    async def another(self, tg_id: int, state: FSMContext | None = NOT_NEW_STATE):
        self.tg_id = tg_id
        if state != NOT_NEW_STATE:
            self.state = state
        return self

    async def text_boardcast(self, tg_ids: list[int], text: str, reply_markup = None, delay: int = 20):
        k = 0
        for tg_id in tg_ids:
            k += 1
            await self.bot.send_message(tg_id, text, reply_markup=reply_markup)
            if k%delay == 0:
                await asyncio.sleep(2)
        return True

    async def texts_boardcast(self, datas: list[tuple[int, str, InlineKeyboardButton | InlineKeyboardMarkup | None, int | None]], delay: int = 20):
        k = 0
        for tg_id, text, reply_markup, message_thread_id in datas:
            k += 1
            await self.bot.send_message(tg_id, text, reply_markup=reply_markup, message_thread_id=message_thread_id)
            if k%delay == 0:
                await asyncio.sleep(2)
        return True

    def to_json(self, msgs: list[tuple[str, BaseValidate, InlineKeyboardButton | InlineKeyboardMarkup | None]]):
        return [(((TextHTML.anchor('start-json') + TextHTML.json_format(self.model_dump(v), 4).pre('json').details('Открыть JSON') + TextHTML('Вверх').href('#start-json')) if self.msg_to_json and v else m),None if self.msg_to_json and v else i) for m, v, i in msgs]

    def model_dump(self, data):
        if hasattr(data, 'model_dump'):
            return data.model_dump()
        elif hasattr(data, '__dict__'):
            return data.__dict__
        elif type(data) == dict:
            return {k:self.model_dump(v) for k, v in data.items()}
        else:
            return str(data)

    def to_pages(self, datas: list[DATA_PAGE], value_in_page: int = 5) -> list[tuple[DATA_PAGE, ...]]:
        return [tuple(datas[i:i+value_in_page]) for i in range(0, len(datas), value_in_page)]
