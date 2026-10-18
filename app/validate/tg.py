from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from app.validate.base import BaseValidate

class AnswerBody(BaseValidate):
    text: str
    data: BaseValidate | None = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None
    is_rich_text: bool = False
    is_reply_answer: bool = False
    edit_message: bool = False

class Answer(AnswerBody):
    chat_tg_id: int
    _user_tg_id: int | None = None
    message_id: int

    @property
    def user_tg_id(self):
        return self._user_tg_id if self._user_tg_id is None else self.chat_tg_id