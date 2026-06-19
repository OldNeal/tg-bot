from aiogram.filters.callback_data import CallbackData

class BaseCall(CallbackData, prefix='base'):
    tg_id: int
    is_check: bool = True

class MenuCall(BaseCall, prefix='menu'):
    where: str
    
class BackCall(BaseCall, prefix='back'):
    where: str



    