from config import settings, bot, Router, Command, FSMContext, Message, flags, ass_tg, timedelta
from app.service.main import MainService

main_router = Router()

@main_router.message(Command('info'))
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    await MainService(message, state).info()