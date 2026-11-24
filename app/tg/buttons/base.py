from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.tg.callback.base import MenuCall, CancelCall, BackCall, MessageDeleteCall
from app.tg.deep.base import MenuDeep

class BotIKB:
    def __init__(self, tg_id: int):
        self.builder = InlineKeyboardBuilder()
        self.tg_id = tg_id
 
    def another_tg_id(self, tg_id: int):
        self.tg_id = tg_id
        return self

    def cancel(self):
        self.builder.button(text='❌ Отменить', callback_data=CancelCall(tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def deep_menu(self, message_id: int | None = None, chat_id: int | None = None):
        return self.builder.button(text='🗨️ Перейти в лс', url=MenuDeep(message_id=message_id, chat_id=chat_id).url()).as_markup()

    def delete_message(self, text: str = '🗑️ Удалить сообщение', text_after: str | None = '🗑️ Сообщение удалено'):
        return self.builder.button(text=text, callback_data=MessageDeleteCall(text=text_after, tg_id=self.tg_id)).as_markup()

    def delete_notify(self):
        return self.delete_message('✔️ Отметить прочитанным', None)

    @property
    def new(self):
        self.builder = InlineKeyboardBuilder()
        return self