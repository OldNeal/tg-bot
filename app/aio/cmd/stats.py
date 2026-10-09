from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage, F, CallbackQuery
from app.service.stats import StatsService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Optionals, Requireds
from app.exception.decor import exept, call_exept
from app.aio.cls.callback.stats import StatsBackCall, BackCall, StatsPageCall, StatsPathsCall
from app.aio.cls.callback.back import StatsBackValues
from app.aio.cls.fsm.state import StatsState
from app.aio.cls.fsm.utils import StatsFSM

stats_router = Router()

@stats_router.message(Command('stats'))
@command(
    name='stats',
    description='Получить статистику', 
    arguments=[Optionals.value] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await StatsService(message, state, **kwargs).all()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@stats_router.callback_query(StatsBackCall.filter(F.where == StatsBackValues.all))  
@call_exept()
async def call(callback: CallbackQuery, callback_data: StatsBackCall, state: FSMContext, **kwargs):
    msgs = await StatsService(callback.message, state, callback, **kwargs).all()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@stats_router.callback_query(StatsPathsCall.filter())  
@call_exept()
async def call(callback: CallbackQuery, callback_data: StatsPathsCall, state: FSMContext, **kwargs):
    msgs = await StatsService(callback.message, state, callback, **kwargs).back_paths()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@stats_router.callback_query(StatsBackCall.filter(F.where == StatsBackValues.stats_paths))  
@stats_router.callback_query(BackCall.filter(F.where == StatsBackValues.stats_paths))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: BackCall, state: FSMContext, **kwargs):
    msgs = await StatsService(callback.message, state, callback, **kwargs).paths()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@stats_router.callback_query(StatsPageCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: StatsPageCall, state: FSMContext, **kwargs):
    msgs = await StatsService(callback.message, state, callback, **kwargs).paths(callback_data.value, callback_data.page)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@stats_router.message(StatsState.search)
@exept()
async def text_state(message: Message, state: FSMContext, **kwargs):
    fsm = StatsFSM(state)
    msg0 = await fsm.get_message()
    msgs = await StatsService(message, state, **kwargs).enter_path()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    await fsm.set_state()
    await bot.delete_message(*msg0)
    await fsm.remove_message()
