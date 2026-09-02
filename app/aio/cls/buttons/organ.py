from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.cls.buttons.base import BotIKB, MenuCall, CancelCall
from app.aio.cls.callback.organ import (OrganBackCall, 
                                        OrganSettingParametrCall, 
                                        OrganSettingRedactCall, 
                                        OrganSettingModeCall, 
                                        OrganSettingGroupCall, 
                                        OrganSettingParametrBooleanCall, 
                                        OrganSettingParametrDefaultCall,
                                        OrganInfoCall,
                                        OrganMemberCall,
                                        OrganInfoDescCall,
                                        OrganInfoMembersCall,
                                        OrganKickCall,
                                        OrganRankRedactCall,
                                        OrganSettingCall,
                                        OrganTitulRedactCall,
                                        OrganExitCall,
                                        OrganLoginCall,
                                        OrganTitulDeleteCall,
                                        OrganPageCall,
                                        OrganCaptureCall,
                                        OrganGiveCall,
                                        OrganMemberPageCall,
                                        OrganSearchCall)
from app.validate.api import OrganSettingValidate, AnswerMemberInfo, OrganInfo, AnswerOrganInfo
from app.aio.cls.callback.back import OrganBackValues


class OrganIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=OrganBackCall(where=where, tg_id=self.tg_id)).as_markup()
    
    def ogr_name(self, name: str, ogr: int = 30):
        return f'{name[:ogr+1]}...' if len(name) > ogr else f'{name}'

    def info(self, data: AnswerOrganInfo, where: str | None = None):
        self.builder.button(text='🪶 Описание', callback_data=OrganInfoDescCall(organ_id=data.organ.id, tg_id=self.tg_id))
        self.builder.button(text='👥 Участники', callback_data=OrganInfoMembersCall(organ_id=data.organ.id, tg_id=self.tg_id))
        if data.for_buttons.is_redact_setting and data.organ.id == data.for_buttons.organ_id:
            self.builder.button(text='⚙️ Настройки', callback_data=OrganSettingCall(tg_id=self.tg_id))
        if data.for_buttons.is_capture and data.for_buttons.is_member and data.organ.id == data.for_buttons.organ_id:
            self.builder.button(text='👑 Захватить власть', callback_data=OrganCaptureCall(tg_id=self.tg_id))
        if data.for_buttons.is_member and data.organ.id == data.for_buttons.organ_id:
            self.builder.button(text='🚪 Выйти', callback_data=OrganExitCall(tg_id=self.tg_id))
        elif not data.for_buttons.is_member:
            self.builder.button(text='🚪 Войти', callback_data=OrganLoginCall(organ_id=data.organ.id, tg_id=self.tg_id))
        if where:
            self.builder.button(text='↩️ Назад', callback_data=OrganBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(2, 1).as_markup()

    def organs(self, organs: list[OrganInfo], page: int, max_page: int, where: str | None = None):
        for organ in organs:
            self.builder.button(text=f'{organ.emodzi or '🏛'} {self.ogr_name(organ.name)}', icon_custom_emoji_id=organ.custom_emodzi_id, callback_data=OrganInfoCall(organ_id=organ.id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=OrganPageCall(page=page-1, is_search=bool(where), tg_id=self.tg_id).pack()))
        if page != max_page - 1 and max_page != 0:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=OrganPageCall(page=page+1, is_search=bool(where), tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)        
        if where:
            self.builder.row(InlineKeyboardButton(text='✒️ Ввести запрос еще раз', callback_data=OrganSearchCall(tg_id=self.tg_id).pack()))
        return self.builder.as_markup()       

    def member(self, data: AnswerMemberInfo):
        row = []
        if data.member.organ_id == data.for_buttons.organ_id and data.user.tg_id != self.tg_id:
            if data.for_buttons.is_redact_rank:
                self.builder.button(text='➕ Повысить', callback_data=OrganRankRedactCall(operation='up', purpose_tg_id=data.user.tg_id, tg_id=self.tg_id))
                self.builder.button(text='➖ Понизить', callback_data=OrganRankRedactCall(operation='down', purpose_tg_id=data.user.tg_id, tg_id=self.tg_id))
                row.append(2)
            if data.for_buttons.is_redact_titul:
                self.builder.button(text='🎖️ Поменять титул', callback_data=OrganTitulRedactCall(purpose_tg_id=data.user.tg_id, tg_id=self.tg_id))
            if data.for_buttons.is_give:
                self.builder.button(text='👑 Передать организацию', callback_data=OrganGiveCall(purpose_tg_id=data.user.tg_id, tg_id=self.tg_id))
            if data.for_buttons.is_kick:
                self.builder.button(text='🚪 Выгнать', callback_data=OrganKickCall(purpose_tg_id=data.user.tg_id, tg_id=self.tg_id))
        row.append(1)
        self.builder.button(text='↩️ Назад', callback_data=OrganInfoMembersCall(organ_id=data.member.organ_id, tg_id=self.tg_id))
        return self.builder.adjust(*row).as_markup()

    def members(self, members: list[AnswerMemberInfo], page: int, max_page: int, organ_id: int):
        for mbr in members:
            self.builder.button(text=f'{mbr.member.rank} - {self.ogr_name(mbr.user.fullname or mbr.user.fullname)} ({mbr.member.rank_name})', callback_data=OrganMemberCall(purpose_tg_id=mbr.user.tg_id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=OrganMemberPageCall(page=page-1, organ_id=organ_id, tg_id=self.tg_id).pack()))
        if page != max_page - 1 and max_page != 0:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=OrganMemberPageCall(page=page+1, organ_id=organ_id, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)        
        self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=OrganInfoCall(organ_id=organ_id, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()       

    def kick(self, purpose: AnswerMemberInfo, is_back: bool = False):
        self.builder.button(text='✅ Да', callback_data=OrganKickCall(accert=True, purpose_tg_id=purpose.user.tg_id, tg_id=self.tg_id))
        if is_back:
            self.builder.button(text='❌ Нет', callback_data=OrganMemberCall(purpose_tg_id=purpose.user.tg_id, tg_id=self.tg_id))
        else:
            self.builder.button(text='❌ Нет', callback_data=OrganKickCall(cancel=True, purpose_tg_id=purpose.user.tg_id, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def redact_titul(self, purpose_tg_id: int, is_back: bool = False):
        self.builder.button(text='🗑️ Удалить титул', callback_data=OrganTitulDeleteCall(purpose_tg_id=purpose_tg_id, tg_id=self.tg_id))
        if is_back:
            self.builder.button(text='❌ Отменить', callback_data=OrganMemberCall(purpose_tg_id=purpose_tg_id, tg_id=self.tg_id))
        else:
            self.builder.button(text='❌ Отменить', callback_data=CancelCall(tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def settings_values(self, is_back: bool):
        self.builder.button(text='✒️ Изменить', callback_data=OrganSettingRedactCall(tg_id=self.tg_id))
        self.builder.button(text='🔩 Сбросить ', callback_data=OrganSettingParametrDefaultCall(is_all=True, tg_id=self.tg_id))
        if is_back:
            self.builder.button(text='↩️ Назад', callback_data=OrganInfoCall(purpose_tg_id=self.tg_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def member_back(self, purpose_tg_id: int):
        self.builder.button(text='↩️ Назад', callback_data=OrganMemberCall(purpose_tg_id=purpose_tg_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def organ_back(self, organ_id: int):
        self.builder.button(text='↩️ Назад', callback_data=OrganInfoCall(organ_id=organ_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def exit(self, organ_id: int | None = None):
        self.builder.button(text='✅ Да', callback_data=OrganExitCall(accert=True, tg_id=self.tg_id))
        if organ_id:
            self.builder.button(text='❌ Нет', callback_data=OrganInfoCall(organ_id=organ_id, tg_id=self.tg_id))
        else:
            self.builder.button(text='❌ Нет', callback_data=OrganExitCall(cancel=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def menu(self):
        self.builder.button(text='🃏 Моя организация', callback_data=OrganInfoCall(purpose_tg_id=self.tg_id, tg_id=self.tg_id))
        self.builder.button(text='🔎 Поиск организаций', callback_data=OrganBackCall(where=OrganBackValues.search, tg_id=self.tg_id))
        self.builder.button(text='📜 Все организации', callback_data=OrganBackCall(where=OrganBackValues.list, tg_id=self.tg_id))
        self.builder.button(text='🏆 Топ организаций', callback_data=OrganBackCall(where=OrganBackValues.top, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def top(self, organs: list[OrganInfo]):
        for n, organ in enumerate(organs, start=1):
            self.builder.button(text=f'{n}. {organ.emodzi or '🏛'} {self.ogr_name(organ.name)} ({organ.member_counts} участ.)', icon_custom_emoji_id=organ.custom_emodzi_id, callback_data=OrganInfoCall(organ_id=organ.id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def give(self, purpose_tg_id: int, is_back: bool = False):
        self.builder.button(text='✅ Да', callback_data=OrganGiveCall(accert=True, purpose_tg_id=purpose_tg_id, tg_id=self.tg_id))
        if is_back:
            self.builder.button(text='❌ Нет', callback_data=OrganMemberCall(purpose_tg_id=purpose_tg_id, tg_id=self.tg_id))
        else:
            self.builder.button(text='❌ Нет', callback_data=OrganGiveCall(cancel=True, purpose_tg_id=purpose_tg_id, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()
