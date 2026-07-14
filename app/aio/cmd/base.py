from config import settings, bot, Router, Command, FSMContext, Message, flags, timedelta, botlog
from app.aio.cmd.main import main_router
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramBadRequest
from app.exception.decor import exept, call_exept

import asyncio

base_router = Router()
base_router.include_routers(main_router)

@base_router.message(Command('chat_id'))
@base_router.message(Command('topic_id'))
@exept
async def cmd_start(message: Message, **kwargs):
    await message.answer(f'Chat id: {message.chat.id}')
    if message.is_topic_message:
        await message.answer(f'\nTopic id: {message.message_thread_id}')    

@base_router.message(Command('cancel'))
@exept
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    await state.set_state()
    await message.answer('✅ Отмена произошла успешно')

@base_router.message(Command('emodzi'))
@exept
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                custom_emoji_id = entity.custom_emoji_id
                await message.answer(f"ID эмодзи: {custom_emoji_id}, эмодзи <tg-emoji emoji-id='{custom_emoji_id}'>🤔</tg-emoji>")
                break

@base_router.message(Command("shutdown"))
async def shutdown_bot(message: Message):
    if message.from_user.id != settings.owner:
        return
    
    await message.answer("🛑 Бот останавливается...")
    await bot.session.close()        
    asyncio.get_running_loop().stop()

