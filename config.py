import os, redis.asyncio as redis
from dotenv import load_dotenv
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (BotCommand,
                           BotCommandScopeChat,
                           BotCommandScopeAllPrivateChats,
                           BotCommandScopeAllGroupChats,
                           BotCommandScopeAllChatAdministrators,
                           User)

load_dotenv(Path(__file__).parent / '.env')

class Settings:
    api_url = os.getenv('api_url')

    bot_token = os.getenv('bot_token')
    dev_bot_token = os.getenv('dev_bot_token', bot_token)
    _is_dev = os.getenv('is_dev', 'f')

    admins = [int(x) for x in os.getenv('admins').split(',')]
    owner = int(os.getenv('owner'))

    _use_proxy = os.getenv('use_proxy', 'f')
    proxy_url = os.getenv('proxy_url')

    _use_redis = os.getenv('use_redis', 'f')
    redis_url = os.getenv('redis_url')
    state_ttl = int(os.getenv('state_ttl', 60*60*24))
    data_ttl = int(os.getenv('data_ttl', 60*60*24))

    redis_host = os.getenv('redis_host', 'localhost')   
    redis_port = int(os.getenv('redis_port', 6379))
    redis_password = os.getenv('redis_password')

    docs_url = os.getenv('docs_url')

    log_files_path = os.getenv('log_files_path', 'logs/')

    info: dict = {}

    @property
    def is_dev(self):
        return True if self._is_dev in ['t', 'true', '1'] else False

    @property
    def token(self):
        return self.dev_bot_token if self.is_dev else self.bot_token

    @property
    def use_redis(self):
        return True if self._use_redis in ['t', 'true', '1'] else False

    @property
    def use_proxy(self):
        return True if self._use_proxy in ['t', 'true', '1'] else False

    @property
    def bot(self) -> User:
        return self.info.get('main')

settings = Settings()

if settings.use_proxy:
    bot_session = AiohttpSession(proxy=settings.proxy_url)
else:
    bot_session = AiohttpSession()

if settings.use_redis:
    storage = RedisStorage(
        redis=redis.from_url(settings.redis_url),
        state_ttl=settings.state_ttl,
        data_ttl=settings.data_ttl
    )
else:
    storage = MemoryStorage()

bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True), session=bot_session)
dp = Dispatcher(storage=storage)

cmds = {
    'info':'💳 Получить свою карточку',

    'member':'🧪 Карточка потустороннего',
    'upseq':'🔝 Продвинуться',
    'time':'⌛ Узнать дату продвижения',
    'kill':'☠️ Потерять контроль',

    'organ':'🏛️ Меню организаций',
    'member':'🎎 Карточка участника',
    'titul':'🎖️ Изменить титул участника',
    'exit':'🚪 Покинуть организацию',
    
    'newspaper':'📰 Меню газет',
    'sub':'🔔 Подписаться на газету',
    'unsub':'🔕 Отписаться от газеты',
    'notify':'📣 Уведомить читателей газеты',

    'wiki':'📚 Меню вики',
    'path':'📜 Информация о путях',
    'ga':'📜 Информация о ВД',
    
    'stats':'📊 Получить статистику',
    'help':'📚 Получить справку',
}

admin_cmds = cmds | {
    'ping':'⌛ Проверить задержку API',
    'downseq':'⬇️ Понизить последовательность',
    'mystate':'🗂️ Ваши куки',
    'mystateclear':'🗑️ Очистить куки',
}

async def to_menu_cmds():
    admin_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in admin_cmds.items()]
    user_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in cmds.items()]
    [await bot.set_my_commands(admin_menu, scope=BotCommandScopeChat(chat_id=admin)) for admin in settings.admins]
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllChatAdministrators())
