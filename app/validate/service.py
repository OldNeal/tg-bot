from app.validate.base import BaseValidate
from config import Message, User

class Purpose(BaseValidate):
    user: User | None = None
    message: Message | None = None
    _tg_id: int | None = None
    _username: str | None = None

    @property
    def tg_id(self):
        return self._tg_id if self._tg_id else self.user.id

    @property
    def username(self):
        return self._username if self._username else self.user.username