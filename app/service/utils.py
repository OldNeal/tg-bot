from config import bot
from aiogram.exceptions import TelegramBadRequest
from functools import wraps
from aiogram.types import Message, CallbackQuery
from aiogram.types.chat_member_banned import ChatMemberStatus

def str_to_json(string: str):
    if ':' not in string:
        raise ValueError("String hasnt ':' ")
    if "'"  in string or "\"" in string:
        string = string.replace("'", '').replace("\"", '')
    if ', 'in string:
        string = string.replace(", ", ',')
    print(string)
    if ',' in string:
        objs = string.split(',')
    else:
        objs = [string]
    
    json = {}
    for obj in objs:
        if ':' in obj:
            if obj.index(':') != 0:
                tpl = obj.split(':')
                print(tpl)
                json |= {tpl[0]: tpl[1]}

    return json

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
    if quan.is_integer() == False:
        raise error_float(f'This user(tg_id={tg_id}) enter float')
    return int(quan)




