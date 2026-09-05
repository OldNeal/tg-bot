from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage
from app.service.help import HelpService
from telegram_click_aio.decorator import command
from app.aio.args import base_args
from app.exception.decor import exept, call_exept

help_router = Router()

@help_router.message(Command('help'))
@command(
    name='help',
    description='Получить список команд',  # <- Описание команды
    arguments=base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await HelpService(message, state).main()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
