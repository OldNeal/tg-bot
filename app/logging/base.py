import loguru, sys, inspect
from functools import wraps
from datetime import time

class BotLog:
    def __init__(self):
        self.loguru = loguru
        self.logger = self.loguru.logger
        self.log_format = """{level.icon}  | <green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan> | <blue>[{extra}]</blue>"""
        self.sinks = self.handlers()
        self.create_handlers()
        self.create_levels()

    def handlers(self):
        return [{
            'sink':sys.stderr,
            'level':'DEBUG',
            'format':self.log_format,
            'enqueue':True,
        }
    ]
    
    def create_handlers(self):
        self.logger.remove()
        id_handlers = []
        for handler in self.sinks:
            l = self.logger.add(**handler)
            id_handlers.append(l)
        return self

    def create_levels(self):
        self.logger.level("MESSAGE", no=15, color="<blue>", icon="💬")
        self.logger.level("BOT START", no=25, color="<white>", icon="🏁")
        self.logger.level("BOT STOP", no=26, color="<white>", icon="🛑")
 
    def decor(self, timer: bool = False, arg: bool = False, logger_kwargs: dict = {}):
        def decorator(func):
            is_async = inspect.iscoroutinefunction(func)
            logger = self.logger.bind(**logger_kwargs, module=func.__module__)
            
            if is_async:
                @wraps(func)
                async def async_wrapped(*args, **kwargs):
                    start_time = time()
                    try:

                        result = await func(*args, **kwargs)
                        end_time = time()

                        log_method = logger.debug if timer else logger.trace
                        log_method(f"Функция {func.__name__} выполнена за {end_time - start_time}")
                        log_method = logger.debug if arg else logger.trace
                        log_method(f"args: {args}, kwargs: {kwargs}")
                        return result
                    except Exception as e:
                        logger.exception(e)
                        raise
                return async_wrapped
            else:
                @wraps(func)
                def sync_wrapped(*args, **kwargs):
                    start_time = time()
                    try:
                        result = func(*args, **kwargs)
                        end_time = time()

                        log_method = logger.debug if timer else logger.trace
                        log_method(f"Функция {func.__name__} выполнена за {end_time - start_time}")
                        log_method = logger.debug if arg else logger.trace
                        log_method(f"args: {args}, kwargs: {kwargs}")
                        return result
                    except Exception as e:
                        logger.exception(e)
                        raise
                return sync_wrapped
        return decorator

    def message(self, msg: int, **kwargs):
        self.logger.log('MESSAGE', f'Text: {msg}', **kwargs)

    def start(self, **kwargs):
        self.logger.log('BOT START', f'Бот запущен', **kwargs)

    def stop(self, **kwargs):
        self.logger.log('BOT STOP', f'Бот останавливается', **kwargs)

botlog = BotLog()
log = botlog.logger