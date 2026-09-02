from app.aio.cls.buttons.base import BotIKB, MenuCall
from app.aio.cls.callback.wiki import WikiBackCall, PathCall, GroupCall, GACall
from app.validate.api import AnswerAllPathInfo, AnswerPathInfo, AnswerGAInfo
from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup


class WikiIKB(BotIKB):    
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=WikiBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def groups_buttons(self, type: str, iter: list[str], group: str | None = None):
        self.builder.row(
            *[InlineKeyboardButton(text=('✅ ' if group == g else '') + g.title(), callback_data=GroupCall(name=g, type=type, tg_id=self.tg_id).pack()) for g in iter],
            width=len(iter))

    def paths_buttons(self, paths: list[AnswerPathInfo], values_in_string: int = 2):
        for path in sorted(paths, key=lambda x: x.path_id):
            self.builder.button(text=path.name, icon_custom_emoji_id=path.custom_emodzi_id, callback_data=PathCall(id=path.path_id, tg_id=self.tg_id))
        self.builder.adjust(values_in_string)

    def all_paths(self, paths: list[AnswerPathInfo], group: str, where: str | None = None):
        groups = self.sorted_groups(set([p.group for p in paths]))
        view_paths = [p for p in paths if p.group == group]
        self.paths_buttons(view_paths)
        self.groups_buttons('path', groups, group)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=WikiBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
    
    def paths(self, paths: list[AnswerPathInfo], where: str | None = None):
        self.paths_buttons(paths)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=WikiBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()

    def gas_buttons(self, gas: list[AnswerGAInfo], values_in_string: int = 2):
        for ga in sorted(gas, key=lambda x: x.ga_id):
            self.builder.button(text=ga.name, icon_custom_emoji_id=ga.custom_emodzi_id, callback_data=GACall(id=ga.ga_id, tg_id=self.tg_id))
        self.builder.adjust(values_in_string)

    def all_gas(self, gas: list[AnswerGAInfo], group: str, where: str | None = None):
        groups = self.sorted_groups(set([g.group for g in gas]))
        view_gas = [g for g in gas if g.group == group]
        self.gas_buttons(view_gas)
        self.groups_buttons('ga', groups, group)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=WikiBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
    
    def gas(self, gas: list[AnswerGAInfo], where: str | None = None):
        self.gas_buttons(gas)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=WikiBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()

    def ga(self, paths: list[AnswerPathInfo], where: str | None = None):
        self.paths_buttons(paths, 1)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=WikiBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
        
    def sorted_groups(self, groups: list[str]):
        return [g for g in groups if g.lower().startswith('зем')] + [g for g in groups if g.lower().startswith('вне')] + [g for g in groups if g.lower().startswith('пар')]
