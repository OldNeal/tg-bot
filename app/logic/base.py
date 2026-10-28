from datetime import datetime

from app.api import client, schemas
from app.logging.base import botlog
from app.exception.base import ApiTimeoutError
from app.logic.utils import class_decor, BaseExceptionResponse
from app.redis.links import links as redis_links

@class_decor
class BaseLogic:
    client = client
    schemas = schemas
    links = redis_links

    def __init__(self, tg_id: int, username: str | None = None, fullname: str | None = None, purpose_tg_id: int | None = None, **kwargs):
        self.tg_id = tg_id
        self.username = username
        self.fullname = fullname
        self.purpose_tg_id = purpose_tg_id or tg_id
        self.kwargs = kwargs

    @property
    async def user_id(self):
        return await self.get_user_id(self.tg_id)

    @property
    async def body(self):
        return self.schemas.QueryBody(user_id=await self.user_id, is_admin=self.is_admin, request_id=self.request_id)

    async def get_user_id(self, tg_id: int):
        user_id = await self.links.get_user_id(tg_id)
        if user_id is None:
            user = await self.client.user_telegram(tg_id=tg_id)
            if isinstance(user, BaseExceptionResponse):
                user = await self.client.user_new(
                    self.schemas.QueryUserUpdate(
                        user_id=0, 
                        request_id=self.request_id, 
                        telegram=self.schemas.TelegramBody(
                            tg_id=tg_id,
                            username=self.username,
                            fullname=self.fullname
                        ))) 
            return user.user_id
        return user_id


    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False)

    @property
    def request_id(self):
        return self.kwargs.get('request_id')

    @property
    def chat_id(self):
        return self.kwargs.get('chat_id')

    async def info(self, purpose_tg_id: int | None = None):
        user_id = await self.get_user_id(purpose_tg_id if purpose_tg_id is not None else self.purpose_tg_id)
        return await self.client.get_info(user_id)
        
    @classmethod
    async def test_api_connect(cls, logged: bool = True):
        try:
            start = datetime.now()
            response = await cls.client.main()
            if response:
                end = datetime.now()
                result = f'{int((end - start).total_seconds()*1000)}'
                if logged:
                    botlog.logger.info('API работает', ping=result, url=cls.client.client.config.base_url)
                return result
            raise ApiTimeoutError('API не работает')
        except:
            raise ApiTimeoutError('API не работает')

    def redact_kwargs(self, **new_kwargs):
        self.kwargs |= new_kwargs
        return self

    def check_is_not_none(self, *objs):
        for obj in objs:
            if not obj is None:
                return obj