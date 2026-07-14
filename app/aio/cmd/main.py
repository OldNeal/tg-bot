from config import settings, bot, Router, Command, FSMContext, Message, flags, timedelta
from app.service.main import MainService
from telegram_click_aio.decorator import command
from app.aio.args import base_args
from app.aio.cmd.beyonder import beyonder_router
from app.exception.decor import exept, call_exept

main_router = Router()
main_router.include_routers(beyonder_router)

@main_router.message(Command('info'))
@command(
    name='info',
    description='Получить карточку',  # <- Описание команды
    arguments=base_args
)
@exept
async def cmd_info(message: Message, state: FSMContext, **kwargs):
    msgs = await MainService(message, state).info()
    [await message.answer(m, reply_markup=k) for m, k in msgs]
