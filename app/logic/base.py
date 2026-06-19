from app.api import client, schemas
from functools import wraps

def decorator(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        result = await method(*args, **kwargs)
        match result:
            case schemas.BaseExceptionResponse() | schemas.HTTPValidationError() | schemas.ValidationError():
                raise result
        return result
    return wrapper

class BaseLogic:
    client = client
    schemas = schemas

    def __init__(self, tg_id: int, username: str | None = None, fullname: str | None = None, purpose_tg_id: int | None = None, **kwargs):
        self.tg_id = tg_id
        self.username = username
        self.fullname = fullname
        self.purpose_tg_id = purpose_tg_id or tg_id
        self.kwargs = kwargs
        self.body = self.schemas.QueryBody(tg_id=self.tg_id, username=self.username, fullname=self.fullname)

    async def info(self, purpose_tg_id: int | None = None):
        return await self.client.get_info(purpose_tg_id or self.purpose_tg_id)