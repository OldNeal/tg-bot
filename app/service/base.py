import asyncio, functools
from datetime import datetime
from typing import TypeVar
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputRichMessage, User, Chat
from aiogram.filters import CommandStart, Command, CommandObject

from config import settings, bot
from app.tg.buttons.base import BotIKB
from app.tg.fsm.utils import FSMUtils
from app.tg.text.base import BaseText
from app.validate.tg import Answer, AnswerBody
from app.logic.base import BaseLogic
from app.logging.base import botlog

NOT_NEW_STATE = object()
DATA_PAGE = TypeVar('DATA_PAGE')

class BaseService:
    asyncio = asyncio
    datetime = datetime
    botlog = botlog

    logic_class: type[BaseLogic] = BaseLogic
    logic: BaseLogic
    fsm_class: type[FSMUtils] = FSMUtils
    fsm: FSMUtils
    ikb_class: type[BotIKB] = BotIKB
    IKB: BotIKB
    text_class: type[BaseText] | None = None
    text: type[BaseText] | None

    def __init__(self,
                 user: User,
                 chat: Chat,
                 message: Message,
                 state: FSMContext | None = None,
                 callback: CallbackQuery | None = None,
                 command: CommandObject | None = None,
                 add_logic_kwargs: dict = {}, 
                 **kwargs):
        self.settings = settings
        self.bot = bot
        self.callback = callback
        self.message = message or self.callback.message
        self.kwargs = kwargs
        self.command = command
        self.state = state

        self.user = user
        self.chat = chat
        self.tg_id = self.user.id
        self.add_logic_kwargs = add_logic_kwargs

        self.fsm = self.fsm_class(self.state)
        self.IKB = self.ikb_class(self.tg_id)
        self.text = self.text_class
        self.logic = self.logic_class(
            tg_id=self.tg_id,
            username=self.user.username,
            fullname=self.user.full_name,
            **self.logic_kwargs
        )

        self.is_bot_message = bool(self.callback)
        self.enter_args: bool = self.command.args != None if command else False
        self.to_edit_message: bool = self.kwargs.get('to_edit_message', bool(self.callback))

    @property
    def logic_kwargs(self):
        return {'is_admin':self.is_admin, 'request_id':self.kwargs.get('request_id'), 'chat_id':self.chat.id, 'purpose_tg_id':self.purpose.id} | self.add_logic_kwargs

    @property
    def purpose(self):
        if self.message.reply_to_message and self.message.is_topic_message and self.kwargs.get('is_reply'):
            return self.message.reply_to_message.from_user
        elif self.message.reply_to_message and not self.message.is_topic_message:
            return self.message.reply_to_message.from_user
        else:
            return self.user

    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False) and self.tg_id_in_admins

    @property
    def tg_id_in_admins(self):
        return self.tg_id in self.settings.admins

    async def text_boardcast(self, answer_body_list: list[Answer], delay: int = 20):
        k = 0
        results: list[Message] = []
        for body in answer_body_list:
            k += 1
            if body.is_reply_answer:
                msg = await self.bot.send_message(text=body.text, reply_markup=body.reply_markup, reply_to_message_id=body.message_id, chat_id=body.chat_tg_id, message_thread_id=body.message_thread_id)
            if body.reply_message_id:
                msg = await self.bot.send_message(text=body.text, reply_markup=body.reply_markup, reply_to_message_id=body.reply_message_id, chat_id=body.chat_tg_id, message_thread_id=body.message_thread_id)
            elif body.is_rich_text and body.edit_message:
                msg = await self.bot.edit_message_text(rich_message=InputRichMessage(html=body.text), reply_markup=body.reply_markup, chat_id=body.chat_tg_id, message_id=body.message_id)
            elif body.is_rich_text:
                msg = await self.bot.send_rich_message(rich_message=InputRichMessage(html=body.text), reply_markup=body.reply_markup, chat_id=body.chat_tg_id, message_thread_id=body.message_thread_id)
            elif body.edit_message:
                msg = await self.bot.edit_message_text(text=body.text, reply_markup=body.reply_markup, chat_id=body.chat_tg_id, message_id=body.message_id)
            else:
                msg = await self.bot.send_message(text=body.text, reply_markup=body.reply_markup, chat_id=body.chat_tg_id, message_thread_id=body.message_thread_id)
            results.append(msg)
            if k%delay == 0:
                await asyncio.sleep(2)
        return results

    def to_pages(self, datas: list[DATA_PAGE], value_in_page: int = 5) -> list[tuple[DATA_PAGE, ...]]:
        return [tuple(datas[i:i+value_in_page]) for i in range(0, len(datas), value_in_page)] if datas else []

    async def answer(self, answer_body_list: list[AnswerBody]):
        return await self.text_boardcast([
            Answer(
                chat_tg_id=self.chat.id,
                _user_tg_id=self.tg_id,
                message_id=self.message.message_id,
                edit_message=self.to_edit_message if body.edit_message is None else None,
                message_thread_id=self.message.message_thread_id,

                text=body.text,
                reply_markup=body.reply_markup,
                is_rich_text=body.is_rich_text,
                is_reply_answer=body.is_reply_answer,
                reply_message_id=body.reply_message_id
                ) for body in answer_body_list
                ])

    def redact_kwargs(self, **new_kwargs):
        self.kwargs |= new_kwargs
        return self