from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup, DisabledButton
from aiogram.enums import ButtonStyle

from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.callback.beyonder import BeyonderInfoCall
from app.tg.callback.main import (
    MainBackCall,
    MainInfoCall,
    MainUserInfoCall,
    MainUserDeleteCall,
    MainUserSettingsCall,
    MainUserSettingsRedactCall,
    MainUserSettingsDefaultCall,
    MainUserSettingsModeCall,
    MainUserSettingEditCall,
    MainUsersCall,
    MainUsersPageCall,
    MainUsersSearchCall,
    MainUsersSearchFieldCall,
    MyStateCall,
)
from app.tg.callback.organ import OrganMemberCall
from app.tg.callback.items import ItemInventoryCall
from app.tg.text.base import BaseText
from app.validate.core import AnswerBaseInfo, AnswerUserBody
from app.tg.settings import is_setting_available, values_by_tag

class MainIKB(BotIKB):    
    search_fields = {
        'user_id': '🏷 Внутренний ID',
        'tg_id': '🆔 Telegram ID',
        'name': '🪦 Имя',
        'username': '🔗 Username',
    }

    def menu(self):
        self.builder.button(text='👤 Аккаунт', callback_data=MenuCall(where='user', tg_id=self.tg_id))
        self.builder.button(text='🏛️ Организации', callback_data=MenuCall(where='organ', tg_id=self.tg_id))
        self.builder.button(text='📰 Газеты', callback_data=MenuCall(where='newspaper', tg_id=self.tg_id))
        self.builder.button(text='📚 Вики', callback_data=MenuCall(where='wiki', tg_id=self.tg_id))
        self.builder.button(text='📯 Викторина', callback_data=MenuCall(where='question', tg_id=self.tg_id))
        self.builder.button(text='📦 Предметы', callback_data=MenuCall(where='items', tg_id=self.tg_id))
        self.builder.button(text='👥 Пользователи', callback_data=MenuCall(where='users', tg_id=self.tg_id))
        self.builder.button(text='📊 Статистика', callback_data=MenuCall(where='stats', tg_id=self.tg_id))
        self.builder.button(text='❔ Справка', callback_data=MenuCall(where='help', tg_id=self.tg_id))
        return self.builder.adjust(1, 2, 2, 2, 2).as_markup()

    def info(self, data: AnswerBaseInfo):
        purpose = data.purpose
        telegram = purpose.telegram if purpose else None
        info_user = purpose or data.user
        info_telegram = info_user.telegram if info_user else None
        if telegram:
            if data.member:
                self.builder.button(
                    text='🏛 Карточка участника',
                    callback_data=OrganMemberCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id),
                )
            self.builder.button(
                text='🔮 Карточка потустороннего',
                callback_data=BeyonderInfoCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id),
            )
        if info_telegram and info_telegram.tg_id == self.tg_id:
            self.builder.button(
                text='🎒 Инвентарь',
                callback_data=ItemInventoryCall(tg_id=self.tg_id),
            )
        self.builder.button(text='👤 Аккаунт', callback_data=MainUserInfoCall(
                    user_id=data.user.user_id,
                    tg_id=self.tg_id,
                ))
        return self.builder.adjust(1).as_markup()

    def user_info(self, data: AnswerBaseInfo):
        purpose = data.purpose
        telegram = purpose.telegram if purpose else None
        if telegram is None:
            return self.builder.as_markup()

        self.builder.button(
                text='🪪 Карточка',
                callback_data=MainInfoCall(purpose_tg_id=telegram.tg_id, tg_id=self.tg_id),
            )
        if telegram.tg_id == self.tg_id:
            self.builder.button(
                text='⚙️ Настройки',
                callback_data=MainUserSettingsCall(tg_id=self.tg_id),
            )
            self.builder.button(
                            text='🗑 Удалить аккаунт',
                            callback_data=MainUserDeleteCall(user_id=purpose.user_id, tg_id=self.tg_id),
                        )
        return self.builder.adjust(1).as_markup()

    def user_settings_editor(self, groups):
        values = values_by_tag(groups)
        for group in groups:
            for parameter in group.parametrs:
                if parameter.is_hidden or not parameter.is_redact or not is_setting_available(parameter, values):
                    continue
                emoji = parameter.emodzi or group.emodzi or '⚙️'
                custom_emoji_id = parameter.custom_emodzi_id or group.custom_emodzi_id
                self.builder.button(
                    text=f'{emoji} {parameter.name}'[:60],
                    icon_custom_emoji_id=custom_emoji_id,
                    callback_data=MainUserSettingEditCall(tag=parameter.tag, tg_id=self.tg_id),
                )
        self.builder.adjust(2)
        self.builder.row(InlineKeyboardButton(text='🔩 Сбросить по умолчанию', callback_data=MainUserSettingsDefaultCall(tg_id=self.tg_id).pack()))
        self.builder.row(InlineKeyboardButton(text='🧾 Редактировать через JSON', callback_data=MainUserSettingsModeCall(is_json=True, tg_id=self.tg_id).pack()))
        self.builder.row(InlineKeyboardButton(text='↩️ К аккаунту', callback_data=MenuCall(where='user', tg_id=self.tg_id).pack()))
        return self.builder.as_markup()

    def user_settings_json(self):
        self.builder.button(
            text='⚙️ Редактировать кнопками',
            callback_data=MainUserSettingsModeCall(is_json=False, tg_id=self.tg_id),
        )
        self.builder.button(
            text='✏️ Изменить через JSON',
            callback_data=MainUserSettingsRedactCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='🔩 Сбросить',
            callback_data=MainUserSettingsDefaultCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='↩️ К аккаунту',
            callback_data=MenuCall(where='user', tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def user_settings_text_prompt(self):
        self.builder.button(
            text='↩️ К настройкам',
            callback_data=MainUserSettingsModeCall(is_json=False, tg_id=self.tg_id),
        )
        return self.builder.as_markup()

    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=MainBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def back_to_list(self):
        return self.builder.button(text='↩️ Назад', callback_data=MainUsersCall(tg_id=self.tg_id)).as_markup()
    
    def my_state(self):
        self.builder.button(text='🔄️ Обновить', callback_data=MyStateCall(tg_id=self.tg_id))
        return self.builder.as_markup()

    def users(self, users: list[AnswerUserBody], page: int, max_page: int):
        for user in users:
            self.builder.button(
                text=f'{user.emodzi if user.emodzi else '👤'} {BaseText.answer_user_name(user)[:24]}',
                icon_custom_emoji_id=user.custom_emodzi_id,
                callback_data=MainUserInfoCall(
                    user_id=user.user_id,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.adjust(1)

        pages = []
        if max_page > 1:
            if page > 0:
                if max_page >= 3:
                    page_back = page - 10
                    pages.append(InlineKeyboardButton(
                        text='⏪',
                        callback_data=MainUsersPageCall(page=page_back if page_back > 0 else 0, tg_id=self.tg_id).pack(),
                    ))
                pages.append(InlineKeyboardButton(
                    text='⬅️',
                    callback_data=MainUsersPageCall(page=page - 1, tg_id=self.tg_id).pack(),
                ))
            else:
                if max_page >= 3:
                    pages.append(InlineKeyboardButton(
                        text='⏪',
                        disabled=DisabledButton(),
                    ))
                pages.append(InlineKeyboardButton(
                    text='⬅️',
                    disabled=DisabledButton(),
                ))
            if page < max_page - 1:
                pages.append(InlineKeyboardButton(
                    text='➡️',
                    callback_data=MainUsersPageCall(page=page + 1, tg_id=self.tg_id).pack(),
                ))
                if max_page >= 3:
                    page_next = page + 10
                    pages.append(InlineKeyboardButton(
                        text='⏩',
                        callback_data=MainUsersPageCall(page=page_next if page_next < max_page - 1 else max_page - 1, tg_id=self.tg_id).pack(),
                    ))
            else:
                pages.append(InlineKeyboardButton(
                    text='➡️',
                    disabled=DisabledButton(),
                ))
                if max_page >= 3:
                    pages.append(InlineKeyboardButton(
                        text='⏩',
                        disabled=DisabledButton(),
                    ))
        if pages:
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(
            text='🔎 Поиск',
            callback_data=MainUsersSearchCall(tg_id=self.tg_id).pack(),
        ))
        self.builder.row(InlineKeyboardButton(
            text='↩️ В меню',
            callback_data=MenuCall(where='main', tg_id=self.tg_id).pack(),
        ))
        return self.builder.as_markup()

    def users_search_fields(self):
        for field, label in self.search_fields.items():
            self.builder.button(
                text=label,
                callback_data=MainUsersSearchFieldCall(
                    field=field,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.adjust(1)
        self.builder.row(InlineKeyboardButton(
            text='↩️ К списку',
            callback_data=MainUsersCall(tg_id=self.tg_id).pack(),
        ))
        return self.builder.as_markup()

    def confirm_user_delete(self, user_id: int):
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text='✅ Да, удалить',
                callback_data=MainUserDeleteCall(
                    user_id=user_id,
                    confirmed=True,
                    tg_id=self.tg_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='❌ Нет, отмена',
                callback_data=MainUserDeleteCall(
                    user_id=user_id,
                    confirmed=False,
                    tg_id=self.tg_id,
                ).pack(),
            ),
        ]])
