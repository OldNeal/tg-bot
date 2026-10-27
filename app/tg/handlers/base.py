from aiogram.types import InputRichMessage, Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import settings, bot
from app.tg.handlers.main import main_router
from app.tg.handlers.help import help_router
from app.tg.text.utils import TextHTML
from app.tg.callback.base import CancelCall
from app.tg.buttons.text import TextKeyboardMarkup, TextKeyboardButton

import asyncio

base_router = Router()
base_router.include_routers(main_router, help_router)

@base_router.message(Command('chat_id'))
@base_router.message(Command('topic_id'))
async def cmd(message: Message):
    await message.answer(f'Chat id: {message.chat.id}')
    if message.is_topic_message:
        await message.answer(f'\nTopic id: {message.message_thread_id}')    

@base_router.message(Command('cancel'))
async def cmd(message: Message, state: FSMContext):
    await state.set_state()
    await message.answer('✅ Отмена произошла успешно')

@base_router.message(Command('emodzi'))
@base_router.message(Command('emoji'))
async def cmd(message: Message):
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
async def cmd(message: Message):
    await message.answer_rich(InputRichMessage(html=TextHTML.example()))

@base_router.message(Command('test'))
async def cmd(message: Message):
    await message.answer_rich(
        InputRichMessage(
            html=TextHTML('Кнопка') + TextKeyboardMarkup([TextKeyboardButton(text='Первая', url=settings.docs_url)]).as_makrup() + TextHTML('Текст после кнопки')
            )
        )

@base_router.callback_query(CancelCall.filter())     
async def call(
    callback: CallbackQuery,
    callback_data: CancelCall,
    state: FSMContext,
):
    text_state = await state.get_state()
    if text_state:
        await state.set_state()
        await callback.message.edit_text(rich_message=InputRichMessage(html='✅ Отмена произошла успешно'), reply_markup=None)
    else:
        await callback.message.edit_text(rich_message=InputRichMessage(html='❗ Вы уже ввели значение'), reply_markup=None)
