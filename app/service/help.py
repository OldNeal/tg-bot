from app.service.base import BaseService
from app.logic.main import MainLogic
from app.aio.cls.msg.help import HelpText
from app.aio.cls.buttons.help import HelpIKB

class HelpService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = MainLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = HelpText
        self.IKB = HelpIKB(tg_id=self.tg_id)

    async def main(self):
        return self.to_json([
            [self.text.main(), None, self.IKB.main()]
            ])
