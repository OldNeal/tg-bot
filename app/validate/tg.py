from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from app.validate.base import BaseValidate

class AnswerBody(BaseValidate):
    text: str
    data: BaseValidate | None = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None
    is_rich_text: bool = False
    is_reply_answer: bool = False
    reply_message_id: int | None = None
    edit_message: bool | None = None

class Answer(AnswerBody):
    chat_tg_id: int
    _user_tg_id: int | None = None
    message_id: int
    message_thread_id: int | None = None

    @property
    def user_tg_id(self):
        return self._user_tg_id if self._user_tg_id is not None else self.chat_tg_id