from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.tg.callback.base import MenuCall, CancelCall, BackCall, MessageDeleteCall
from app.tg.deep.base import MenuDeep
from app.tg.settings import visible_setting_groups

class BotIKB:
    def __init__(self, tg_id: int):
        self.builder = InlineKeyboardBuilder()
        self.tg_id = tg_id
 
    def another_tg_id(self, tg_id: int):
        self.tg_id = tg_id
        return self

    def setting_groups(self, groups, group_tag: str | None, callback_factory, reset_callback=None):
        if reset_callback is not None:
            self.builder.row(InlineKeyboardButton(
                text='🔩 Сбросить группу',
                callback_data=reset_callback.pack(),
            ))
        buttons = []
        for group in visible_setting_groups(groups):
            marker = '✅ ' if group.tag == group_tag else ''
            buttons.append(InlineKeyboardButton(
                text=f'{marker}{group.emodzi or "⚙️"} {group.name}'[:60],
                icon_custom_emoji_id=group.custom_emodzi_id,
                callback_data=callback_factory(group.tag).pack(),
            ))
        if buttons:
            self.builder.row(*buttons, width=4)

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
