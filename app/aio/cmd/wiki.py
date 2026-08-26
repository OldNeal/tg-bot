from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage, F, CallbackQuery
from app.service.wiki import WikiService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Optionals, Requireds
from app.exception.decor import exept, call_exept
from app.aio.cls.callback.wiki import PathCall, GroupCall, WikiBackCall, GACall

wiki_router = Router()

@wiki_router.message(Command('ga'))
@command(
    name='ga',
    description='Получить информацию о великих древних', 
    arguments=[Optionals.value] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await WikiService(message, state, **kwargs).ga()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(GroupCall.filter(F.type == 'ga'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: GroupCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).all_gas(callback_data.name)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(GACall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: PathCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).get_ga(id=callback_data.id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiBackCall.filter(F.where == 'gas'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).back_ga()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiBackCall.filter(F.where == 'ga'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).get_ga()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

#@wiki_router.message(Command('seq'))
#@command(
#    name='seq',
#    description='Получить карточку', 
#    arguments=base_args
#)
#async def cmd_start(message: Message, state: FSMContext, **kwargs):
#    msgs = await WikiService(message, state, **kwargs).info()
#    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.message(Command('path'))
@command(
    name='path',
    description='Получить информацию о путях', 
    arguments=[Optionals.value] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await WikiService(message, state, **kwargs).path()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(GroupCall.filter(F.type == 'path'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: GroupCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).all_paths(callback_data.name)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(PathCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: PathCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).get_path(id=callback_data.id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiBackCall.filter(F.where == 'paths'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).back_path()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]



