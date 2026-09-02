from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage, F, CallbackQuery
from app.service.stats import StatsService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Optionals, Requireds
from app.exception.decor import exept, call_exept

stats_router = Router()

@stats_router.message(Command('stats'))
@command(
    name='stats',
    description='Получить статистику', 
    arguments=base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await StatsService(message, state, **kwargs).all()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
