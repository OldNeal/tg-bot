from app.logging.base import log, botlog
from typing import Literal    

class PythonError:
    msg = '⚠️ Непредвиденная ошибка'

class BotError(Exception):
    msg = 'Базовый класс ошибки'
    faq = ''
    emodzi = '⚠️'

    def __init__(self, *args, level: Literal['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'] = 'warning', is_error: bool = True, **kwargs):
        self.level = level
        self.args = args
        self.kwargs = kwargs
        self.is_error = is_error
        if is_error:
            super().__init__(*args)
            getattr(log, level)(f'{self.__class__.__name__}, msg: {' '.join([self.args])}, kwargs: {self.kwargs}')

    def __str__(self):
        return super().__str__()
    
    @property
    def to_msg(self):
        return f'{self.emodzi} {self.name}: {self.msg}'
     
    @property
    def name(self):
        return self.__class__.__name__

class PermissionError(BotError):
    msg = 'У вас нет доступа'
    emodzi = '❌'

class ALienCallbackError(BotError):
    msg = 'Это не ваша кнопка'
    emodzi = '❌'

class ApiError(BotError):
    msg = None

    def __init__(self, *args, level = 'warning', is_error = True, **kwargs):
        super().__init__(*args, level=level, is_error=is_error, **kwargs)
        self.msg = ' '.join([self.args])

    @property
    def to_msg(self):
        return self.msg

def msg_error(bot_error: BotError | list[BotError]) -> str | list[str]:
    if type(bot_error) == BotError: return bot_error.to_msg()
    elif type(bot_error) == list:
        return [e.to_msg() for e in bot_error]
    else:
        raise AttributeError(f'Error to msg_error, bot error: {bot_error}')
    

def get_sub_exeptions(cls):

    """Рекурсивно получаем все дочерние классы"""
    all_subclasses = []
    
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_sub_exeptions(subclass))
    
    return all_subclasses

def get_error_faq() -> dict[str, BotError]: 
    error_faq: dict[str, BotError] = {}
    sub_exeptions: list[BotError] = get_sub_exeptions(BotError)
    for error in sub_exeptions:
        error_faq |= {error.code: error}
    return error_faq

