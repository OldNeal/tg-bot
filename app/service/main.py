from app.service.base import BaseService
from app.logic.main import MainLogic

class MainService(BaseService):
    def __init__(self, message = None, state = None, callback = None, purpose_tg_id = None, **kwargs):
        super().__init__(message, state, callback, purpose_tg_id, **kwargs)
        self.logic = MainLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, purpose_tg_id=self.purpose_tg_id, **self.kwargs)
        
    async def info(self):
        data = await self.logic.info()
        await self.message.answer(data.model_dump_json())

