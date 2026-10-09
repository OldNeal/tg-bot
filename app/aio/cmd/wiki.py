from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage, F, CallbackQuery
from app.service.wiki import WikiService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Optionals, Requireds
from app.exception.decor import exept, call_exept
from app.aio.cls.callback.wiki import PathCall, GroupCall, WikiBackCall, GACall, WikiMenuCall, WikiSearchCall, PathsPageCall, GasPageCall
from app.aio.cls.callback.back import WikiBackValues
from app.aio.cls.fsm.state import WikiState
from app.aio.cls.fsm.utils import WikiFSM

wiki_router = Router()

@wiki_router.message(Command('wiki'))
@command(
    name='wiki',
    description='Вызвать вики-меню', 
    arguments=base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await WikiService(message, state, **kwargs).menu()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiMenuCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiMenuCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).menu(callback_data.type)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.menu))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).menu()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    
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
async def call(callback: CallbackQuery, callback_data: GACall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).get_ga(id=callback_data.id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.gas))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).back_ga(callback_data.is_all)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.ga))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).get_ga()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

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

@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.search))   
@wiki_router.callback_query(WikiBackCall.filter(F.where == WikiBackValues.paths))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiBackCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).back_path(callback_data.is_all)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(WikiSearchCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: WikiSearchCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).to_enter_search_value(callback_data.type)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.message(WikiState.search)
@exept()
async def text_state(message: Message, state: FSMContext, **kwargs):
    fsm = WikiFSM(state)
    msg0 = await fsm.get_message()
    msgs = await WikiService(message, state, **kwargs).enter_search_value()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    await fsm.set_state()
    await bot.delete_message(*msg0)
    await fsm.remove_message()

@wiki_router.callback_query(PathsPageCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: PathsPageCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).search_path(value=callback_data.value, page=callback_data.page)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.callback_query(GasPageCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: GasPageCall, state: FSMContext, **kwargs):
    msgs = await WikiService(callback.message, state, callback, **kwargs).search_ga(value=callback_data.value, page=callback_data.page)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
