from app.api import client, schemas
from functools import wraps
from datetime import datetime
from app.logging.base import log
from app.exception.base import ApiTimeoutError
from app.logic.utils import class_decor

@class_decor
class BaseLogic:
    client = client
    schemas = schemas

    def __init__(self, tg_id: int, username: str | None = None, fullname: str | None = None, purpose_tg_id: int | None = None, **kwargs):
        self.tg_id = tg_id
        self.username = username
        self.fullname = fullname
        self.purpose_tg_id = purpose_tg_id or tg_id
        self.kwargs = kwargs
        self.body = self.schemas.QueryBody(tg_id=self.tg_id, username=self.username, fullname=self.fullname, is_admin=self.is_admin)

    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False)

    async def info(self, purpose_tg_id: int | None = None):
        return await self.client.get_info(purpose_tg_id or self.purpose_tg_id)
        
    @classmethod
    async def test_api_connect(cls, logged: bool = True):
        try:
            start = datetime.now()
            response = await cls.client.main()
            if response:
                end = datetime.now()
                result = f'{int((end - start).total_seconds()*1000)}'
                if logged:
                    log.info('API работает', ping=result, url=cls.client.client.config.base_url)
                return result
            raise ApiTimeoutError('API не работает')
        except:
            raise ApiTimeoutError('API не работает')

