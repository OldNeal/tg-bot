from app.service.base import BaseService
from app.logic.main import MainLogic
from app.aio.cls.msg.help import HelpText

class HelpService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = MainLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, purpose_tg_id=self.purpose.id, **self.logic_kwargs)
        self.text = HelpText

    async def main(self):
        return self.to_json([
            [self.text.main(), None, None]
            ])
