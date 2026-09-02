from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage, CallbackQuery
from app.aio.cmd.main import main_router
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramBadRequest
from app.exception.decor import exept, call_exept
from app.aio.cls.msg.utils import TextHTML
from app.aio.cls.callback.base import CancelCall

import asyncio

base_router = Router()
base_router.include_routers(main_router)

@base_router.message(Command('chat_id'))
@base_router.message(Command('topic_id'))
@exept()
async def cmd(message: Message, **kwargs):
    await message.answer(f'Chat id: {message.chat.id}')
    if message.is_topic_message:
        await message.answer(f'\nTopic id: {message.message_thread_id}')    

@base_router.message(Command('cancel'))
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    await state.set_state()
    await message.answer('✅ Отмена произошла успешно')

@base_router.message(Command('emodzi'))
@base_router.message(Command('emoji'))
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    text = []
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                custom_emoji_id = entity.custom_emoji_id
                text.append(f"ID эмодзи: {TextHTML(custom_emoji_id).code()}, эмодзи {TextHTML('🃏').custom_emoji(f'{custom_emoji_id}')}")
        await message.answer('\n'.join(text))

@base_router.message(Command("shutdown"))
async def cmd(message: Message):
    if message.from_user.id != settings.owner:
        return
    
    await message.answer("🛑 Бот останавливается...")
    await bot.session.close()        
    asyncio.get_running_loop().stop()

@base_router.message(Command('rich'))
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    await message.answer_rich(InputRichMessage(html=TextHTML.example()))

@base_router.message(Command('test'))
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    await message.answer_rich(InputRichMessage(html=TextHTML("""<tag>Tag</tag>, a & b, "quotes", 'single'""").pre()))

@base_router.callback_query(CancelCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: CancelCall, state: FSMContext, **kwargs):
    await state.set_state()
    await callback.message.edit_text(rich_message=InputRichMessage(html='✅ Отмена произошла успешно'), reply_markup=None)