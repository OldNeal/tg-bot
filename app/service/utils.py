from telegram_click_aio.error_handler import ErrorHandler
from aiogram.types import Message

def is_natural_int(string: str | None, 
                   tg_id: int | None = None, 
                   error_less_one = ValueError,
                   error_float = ValueError,
                   error_no_int = ValueError,
                   error_group = Exception) -> int:
    try:
        quan = float(string)
    except ValueError:
        raise error_no_int(f'This user(tg_id={tg_id}) enter no int')
    if quan <= 0:
        raise error_less_one(f'This user(tg_id={tg_id}) enter int, but int <=0: {string}')
    if not quan.is_integer():
        raise error_float(f'This user(tg_id={tg_id}) enter float')
    return int(quan)

class RaiseErrorHandler(ErrorHandler):
    async def on_execution_error(message: Message, error: Exception):
        raise error


