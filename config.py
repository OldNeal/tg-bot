from dotenv import load_dotenv
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (BotCommand, 
                           BotCommandScopeChat, 
                           BotCommandScopeAllPrivateChats, 
                           BotCommandScopeAllGroupChats, 
                           BotCommandScopeAllChatAdministrators,
                           InputRichMessage, 
                           Message, 
                           CallbackQuery, 
                           User)
from aiogram import Bot, Dispatcher, Router, F, flags
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from datetime import timedelta, datetime
from app.logging.base import botlog, log

load_dotenv(Path(__file__).parent / '.env')

class Settings:
    api_url = os.getenv('api_url')
    bot_token = os.getenv('bot_token')
    dev_bot_token = os.getenv('dev_bot_token')
    is_dev_str = os.getenv('is_dev', 'f')
    admins = [int(x) for x in os.getenv('admins').split(',')]
    owner = int(os.getenv('owner'))
    news_group_id = int(os.getenv('news_group'))
    logs_group_id = int(os.getenv('logs_group'))

    @property
    def is_dev(self):
        return True if self.is_dev_str in ['t', 'true', '1'] else False

    @property
    def token(self):
        return self.bot_token if not(self.is_dev) else self.dev_bot_token

settings = Settings()

bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))
dp = Dispatcher(storage=MemoryStorage())

cmds = {
    'info':'💳 Получить карточку персонажа',

    'drink':'🧪 Выпить зелье',
    'upseq':'🔝 Продвинуться',
    'time':'⌛ Узнать время продвижения',
    'kill':'☠️ Потерять контроль',

    'path':'📜 Информация о путях',
    'stats':'📊 Получить статистику',
    'help':'📚 Получить справку',
    'ping':'⌛ Проверить задержку API',
}

admin_cmds = cmds | {
    'dowseq':'⬇️ Понизить последовательность',
}

async def to_menu_cmds():
    admin_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in admin_cmds.items()]
    user_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in cmds.items()]
    [await bot.set_my_commands(admin_menu, scope=BotCommandScopeChat(chat_id=admin)) for admin in settings.admins]
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllChatAdministrators())
