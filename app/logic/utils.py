from functools import wraps
from app.exception.base import ApiError
from app.validate.api import BaseExceptionResponse

def class_decor(cls):
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, api_error_decor(method))
    return cls

def api_error_decor(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) == BaseExceptionResponse:
            raise ApiError(result.message)
        return result
    return wrapped



