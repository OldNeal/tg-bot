import inspect
from functools import wraps
from httpx2 import ConnectError

from app.exception.base import CoreError, CoreTimeoutError
from app.validate.core import BaseExceptionResponse

def class_decor(cls):
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, core_error_decor(method))
    return cls

def core_error_decor(func):
    is_async = inspect.iscoroutinefunction(func)
    if is_async:
        @wraps(func)
        async def async_wrapped(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if type(result) == BaseExceptionResponse:
                    raise CoreError(result.message, status_code=result.status_code)
                return result
            except ConnectError:
                raise CoreTimeoutError('CORE не работает')
        return async_wrapped
    else:
        @wraps(func)
        def sync_wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if type(result) == BaseExceptionResponse:
                    raise CoreError(result.message, status_code=result.status_code)
                return result
            except ConnectError:
                raise CoreTimeoutError('CORE не работает')
        return sync_wrapped


