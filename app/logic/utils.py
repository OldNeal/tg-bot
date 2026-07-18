from functools import wraps
from app.exception.base import ApiError, ApiTimeoutError
from app.validate.api import BaseExceptionResponse
from httpx2 import ConnectError
import inspect

def class_decor(cls):
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, api_error_decor(method))
    return cls

def api_error_decor(func):
    is_async = inspect.iscoroutinefunction(func)
    if is_async:
        @wraps(func)
        async def async_wrapped(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if type(result) == BaseExceptionResponse:
                    raise ApiError(result.message)
                return result
            except ConnectError:
                raise ApiTimeoutError('API не работает')
        return async_wrapped
    else:
        @wraps(func)
        def sync_wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if type(result) == BaseExceptionResponse:
                    raise ApiError(result.message)
                return result
            except ConnectError:
                raise ApiTimeoutError('API не работает')
        return sync_wrapped


