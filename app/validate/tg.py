from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, EphemeralMessageParameters

from app.validate.base import BaseValidate

class AnswerBody(BaseValidate):
    text: str
    data: BaseValidate | None = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None
    is_rich_text: bool = False
    is_reply_answer: bool = False
    reply_message_id: int | None = None
    edit_message: bool | None = None
    is_ephemeral: bool = False
    is_replace_callback_query_message: bool | None = None
    is_send_to_private: bool = False    

class Answer(AnswerBody):
    chat_tg_id: int
    user_tg_id: int
    message_id: int
    message_thread_id: int | None = None
    callback_id: str | None = None

    @property
    def send_tg_id(self):
        return self.user_tg_id if self.is_send_to_private else self.chat_tg_id

    @property
    def ephemeral_message_parameters(self):
        if self.is_ephemeral and not self.is_send_to_private:
            return EphemeralMessageParameters(
                receiver_user_id=self.user_tg_id,
                callback_query_id=self.callback_id,
                replace_callback_query_message=self.is_replace_callback_query_message
            )
        