from aiogram.fsm.context import FSMContext
from app.aio.cls.buttons.base import BotIKB
from config import settings, bot
from app.aio.cls.fsm.utils import FSMUtils
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from app.service.utils import is_natural_int
import datetime

NOT_NEW_STATE = object()

class BaseService:
    def __init__(self, 
                 message: Message | None = None, 
                 state: FSMContext | None = None, 
                 callback: CallbackQuery | None = None, 
                 purpose_tg_id: int | None = None,
                 **kwargs):
        self.settings = settings
        self.bot = bot
        self.message = message
        self.callback = callback
        self.kwargs = kwargs

        self.user = self.callback.from_user if self.callback else self.message.from_user
        self.tg_id = self.user.id
        self.purpose_message = message.reply_to_message
        self.purpose = self.purpose_message.from_user if self.purpose_message else self.user
        self.purpose_tg_id = purpose_tg_id or self.purpose.id or self.tg_id
        
        self.state: FSMUtils = FSMUtils(state)
        self.IKB = BotIKB(self.tg_id)
        self.logic = None
        self.asyncio = asyncio
        self.datetime = datetime
    
    @classmethod
    def is_natural_int(self, value, **kwargs):
        return is_natural_int(value, **kwargs)

    async def get_news_channel_info(self):
        channel = await self.bot.get_chat(self.settings.news_group_ids)
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


