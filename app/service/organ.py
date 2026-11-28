import json, json5

from app.service.base import BaseService, AnswerBody
from app.logic.organ import OrganLogic
from app.tg.text.organ import OrganText
from app.tg.buttons.organ import OrganIKB
from app.tg.fsm.state import OrganState
from app.tg.fsm.utils import OrganFSM
from app.tg.callback.back_values import OrganBackValues
from app.exception.organ import OrganPermissioError
from app.exception.base import JSONEnterError
from app.tg.settings import coerce_setting_input, is_setting_available, selected_setting_group, values_by_tag

class OrganService(BaseService):
    logic_class: type[OrganLogic] = OrganLogic
    logic: OrganLogic
    text_class: type[OrganText] = OrganText
    text: type[OrganText]
    ikb_class: type[OrganIKB] = OrganIKB
    IKB: OrganIKB
    fsm_class: type[OrganFSM] = OrganFSM
    fsm: OrganFSM

    async def menu(self):
        await self.fsm.set_state()
        await self.fsm.remove_value('back_where2')
        return await self.answer([
            AnswerBody(
                text=self.text.menu(),
                reply_markup=self.IKB.menu(),
            )
        ])

    async def my_organ(self):
        try:
            await self.fsm.update_data(back_where2=OrganBackValues.menu)
            return await self.info()
        except Exception:
            return await self.answer([
                AnswerBody(
                    text=self.text.my_organ(),
                    reply_markup=self.IKB.my_organ()
                )
            ])

    async def member(self, purpose_tg_id: int | None = None):
        await self.fsm.set_state()
        if purpose_tg_id is None:
            purpose_tg_id = self.purpose.id
        data = await self.logic.member(purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.member(data),
                data=data,
                reply_markup=self.IKB.member(data),
            )
        ])

    async def info(self, organ_id: int | None = None, purpose_tg_id: int | None = None, is_back: bool = False):
        back_where2 = await self.fsm.pop_value('back_where2')
        organ_id = organ_id if not organ_id is None else await self.fsm.get_value('organ_id')
        data = await self.logic.info(organ_id=organ_id,purpose_tg_id=purpose_tg_id,)
        return await self.answer([
            AnswerBody(
                text=self.text(data).info,
                data=data,
                reply_markup=self.IKB.info(data, where=back_where2),
            )
        ])

    async def delete_organ(self, organ_id: int, confirmed: bool = False):
        if not confirmed:
            data = await self.logic.info(organ_id=organ_id)
            return await self.answer([AnswerBody(
                text=f'❓ Удалить организацию «{data.organ.name}»? Это действие нельзя отменить.',
                data=data,
                reply_markup=self.IKB.confirm_delete(organ_id),
            )])
        await self.logic.delete(organ_id)
        await self.fsm.remove_value('organ_id')
        return await self.menu()

    async def search(self, value: str | None = None, is_new_search: bool = False, page: int | None = None):
        page = page if page is not None else await self.fsm.get_value('page', 0)
        value = await self.fsm.pop_value('search_value', value)
        if value and not is_new_search:
            data = await self.logic.search(value=value, page=page)
        else:
            return await self.to_enter_search()
        max_page = data.page.max
        page = data.page.number
        if len(data.organs) == 0:
            await self.fsm.update_data(back_where2=OrganBackValues.search,page=page,)
        else:
            await self.fsm.update_data(
                search_value=data.search_value,
                back_where2=OrganBackValues.search,
                page=page,
            )
        return await self.answer([
            AnswerBody(text=self.text.search(data.search_value, data.count, page, max_page),
                data=data,
                reply_markup=self.IKB.organs(data.organs, page, max_page, OrganBackValues.search),
            )
        ])

    async def to_enter_search(self):
        await self.fsm.set_state(OrganState.search)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_search(),
                reply_markup=self.IKB.back_menu(),
            )
        ])

    async def to_search(self):
        return await self.search(self.message.text, page=0)

    async def enter_search(self):
        await self.fsm.remove_value('search_value')
        return await self.search()

    async def info_members(self, organ_id: int, page: int | None = None):
        page = page if page is not None else await self.fsm.get_value('info_members_page', 0)
        data = await self.logic.info_members(organ_id=organ_id, page=page)
        max_page = data.page.max
        page = data.page.number
        await self.fsm.update_data(organ_id=data.id, info_members_page=page)
        return await self.answer([
            AnswerBody(
                text=self.text(data).members(page, max_page),
                data=data,
                reply_markup=self.IKB.members(data.members, page, max_page, data.id),
            )
        ])

    async def info_description(self, organ_id: int):
        data = await self.logic.info_description(organ_id=organ_id)
        await self.fsm.update_data(organ_id=data.id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).desc,
                data=data,
                reply_markup=self.IKB.organ_back(data.id),
            )
        ])

    async def list(self, page: int | None = None):
        page = page if page is not None else await self.fsm.get_value('page', 0)
        data = await self.logic.list(page=page)
        max_page = data.page.max
        page = data.page.number
        await self.fsm.update_data(back_where2=OrganBackValues.list, page=page)
        return await self.answer([
            AnswerBody(
                text=self.text.list(page, max_page),
                data=data,
                reply_markup=self.IKB.organs(data.organs, page, max_page),
            )
        ])

    async def top(self):
        data = await self.logic.top_members()
        await self.fsm.update_data(back_where2=OrganBackValues.top)
        return await self.answer([
            AnswerBody(
                text=self.text.top(),
                data=data,
                reply_markup=self.IKB.top(data.organs),
            )
        ])

    async def login(self, organ_id: int | None = None, name: str | None = None):
        if organ_id:
            data = await self.logic.login(organ_id=organ_id)
            return await self.answer([
                AnswerBody(
                    text=self.text(data).login,
                    data=data,
                    reply_markup=self.IKB.organ_back(data.organ.id)
                )
            ])
        if name:
            data = await self.logic.search(value=name, page=0)
            page = data.page.number
            max_page = data.page.max
            await self.fsm.update_data(search_value=data.search_value or name, page=page)
            return await self.answer([
                AnswerBody(
                    text=self.text.search(data.search_value or name, data.count, page, max_page),
                    data=data,
                    reply_markup=self.IKB.organs(data.organs, page, max_page, 'login'),
                )
            ])
        return await self.search()

    async def to_exit(self):
        data = await self.logic.info()
        return await self.answer([
            AnswerBody(
                text=self.text.to_exit(),
                data=data,
                reply_markup=self.IKB.exit(data.organ.id),
            )
        ])

    async def exit(self):
        data = await self.logic.exit()
        return await self.answer([
            AnswerBody(
                text=self.text(data).exit,
                data=data,
                reply_markup=self.IKB.organ_back(data.organ.id),
            )
        ])

    async def cancel_exit(self):
        data = await self.logic.info()
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_exit,
                data=data,
            )
        ])

    async def create(self, name: str):
        if name:
            data = await self.logic.create(name=name)
            return await self.answer([
                AnswerBody(
                    text=self.text(data).create,
                    data=data,
                    reply_markup=self.IKB.create(data.organ.id)
                )
            ])
        return await self.to_enter_name_for_create()

    async def to_enter_name_for_create(self):
        try:
            await self.logic.info()
        except Exception:
            await self.fsm.set_state(OrganState.create)
            await self.fsm.save_message(self.message.chat.id, self.message.message_id)
            return await self.answer([
                AnswerBody(
                    text=self.text.to_create(),
                    reply_markup=self.IKB.cancel()
                )
            ])
        raise OrganPermissioError()

    async def enter_name_for_create(self):
        return await self.create(self.message.text)

    async def get_settings(self, is_json: bool | None = None, group_tag: str | None = None):
        await self.fsm.set_state()
        await self.fsm.remove_value('setting_tag')
        if is_json is None:
            is_json = await self.fsm.get_value('organ_settings_json', False)
        await self.fsm.update_data(organ_settings_json=is_json)
        data = await self.logic.settings_detail()
        values = {
            parameter.tag: parameter.value
            for group in data.settings.groups
            for parameter in group.parametrs
        }
        if is_json:
            return await self.answer([
                AnswerBody(
                    text=self.text(data).settings_values(values),
                    data=data,
                    reply_markup=self.IKB.settings_json(self.is_bot_message),
                    is_rich_text=True,
                )
            ])
        if group_tag is None:
            group_tag = await self.fsm.get_value('organ_settings_group')
        selected = selected_setting_group(data.settings.groups, group_tag)
        group_tag = selected.tag if selected else None
        await self.fsm.update_data(organ_settings_group=group_tag)
        return await self.answer([
            AnswerBody(
                text=self.text.settings_editor(data.settings.groups, group_tag),
                data=data,
                reply_markup=self.IKB.settings_values(self.is_bot_message, data.settings.groups, group_tag)
            )
        ])

    async def setting_subparameters(self, tag: str):
        data = await self.logic.settings_detail()
        parameter = next((
            parameter
            for group in data.settings.groups
            for parameter in group.parametrs
            if parameter.tag == tag and parameter.subparameters
        ), None)
        if parameter is None:
            return await self.get_settings()
        return await self.answer([
            AnswerBody(
                text=self.text(data).settings_subparameters(parameter),
                data=data,
                reply_markup=self.IKB.settings_subparameters(parameter)
            )
        ])

    async def edit_setting_subparameter(self, tag: str, subtag: str | None = None):
        if subtag is None:
            return await self.setting_subparameters(tag)
        data = await self.logic.settings_detail()
        setting_values = values_by_tag(data.settings.groups)
        parameter = next((
            parameter
            for group in data.settings.groups
            for parameter in group.parametrs
            if parameter.tag == tag and is_setting_available(parameter, setting_values)
        ), None)
        subparameter = next((
            subparameter for subparameter in (parameter.subparameters or [])
            if subparameter.tag == subtag and subparameter.is_redact and not subparameter.is_hidden
        ), None) if parameter else None
        if parameter is None or subparameter is None:
            return await self.get_settings()

        current = parameter.value.get(subtag, subparameter.default_value)
        if subparameter.type_ == 'bool' and isinstance(current, bool):
            await self.save_setting_subparameter(tag, subtag, not current)
            return await self.setting_subparameters(tag)

        await self.fsm.set_state(OrganState.setting_subparameter)
        await self.fsm.update_data(setting_tag=tag, setting_subtag=subtag)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([AnswerBody(
            text=f'✒️ Введите новое значение для «{subparameter.name}»',
            reply_markup=self.IKB.settings_subparameter_prompt(
                tag,
                subtag,
                has_default=not subparameter.is_default_value,
            ),
        )])

    async def save_setting_subparameter(self, tag: str, subtag: str, value):
        data = await self.logic.settings()
        values = data.values
        parent_value = dict(values.get(tag) or {})
        parent_value[subtag] = value
        values[tag] = parent_value
        await self.logic.settings_redact(values)

    async def redact_setting_subparameter(self):
        tag = await self.fsm.get_value('setting_tag')
        subtag = await self.fsm.get_value('setting_subtag')
        if not tag or subtag is None:
            await self.fsm.set_state()
            return await self.get_settings()
        data = await self.logic.settings_detail()
        parameter = next((
            parameter
            for group in data.settings.groups
            for parameter in group.parametrs
            if parameter.tag == tag
        ), None)
        subparameter = next((
            subparameter for subparameter in (parameter.subparameters or [])
            if subparameter.tag == subtag
        ), None) if parameter else None
        if subparameter is None:
            await self.fsm.set_state()
            return await self.get_settings(is_json=False)
        try:
            value = coerce_setting_input(self.message.text or '', subparameter)
        except ValueError as error:
            await self.answer([AnswerBody(
                text=f'⚠️ {error}',
                reply_markup=self.IKB.settings_subparameter_prompt(
                    tag,
                    subtag,
                has_default=not subparameter.is_default_value,
                ),
            )])
            return False
        await self.save_setting_subparameter(tag, subtag, value)
        msg0 = await self.fsm.get_message()
        await self.fsm.set_state()
        if all(msg0):
            await self.bot.delete_message(*msg0)
        await self.fsm.remove_value('setting_tag')
        await self.fsm.remove_value('setting_subtag')
        await self.fsm.remove_message()
        return await self.setting_subparameters(tag)

    async def default_settings_group(self, group_tag: str):
        await self.logic.settings_default(group=group_tag, is_all=False)
        await self.callback.answer('⚙️ Настройки группы сброшены')
        return await self.get_settings(is_json=False, group_tag=group_tag)

    async def default_settings(
        self,
        tag: str | None = None,
        subtag: str | None = None,
        is_all: bool = False,
    ):
        if subtag is not None and tag is not None:
            detail = await self.logic.settings_detail()
            parent = next((
                parameter
                for group in detail.settings.groups
                for parameter in group.parametrs
                if parameter.tag == tag
            ), None)
            subparameter = next((
                subparameter for subparameter in (parent.subparameters or [])
                if subparameter.tag == subtag
            ), None) if parent else None
            if subparameter is None:
                return await self.get_settings(is_json=False)
            await self.save_setting_subparameter(tag, subtag, getattr(subparameter, 'default_value', None))
            await self.fsm.set_state()
            await self.fsm.remove_value('setting_tag')
            await self.fsm.remove_value('setting_subtag')
            await self.fsm.remove_message()
            await self.callback.answer('⚙️ Параметр сброшен')
            return await self.setting_subparameters(tag)

        if tag is not None and not is_all:
            detail = await self.logic.settings_detail()
            values = values_by_tag(detail.settings.groups)
            parameter = next((
                parameter
                for group in detail.settings.groups
                for parameter in group.parametrs
                if parameter.tag == tag
            ), None)
            if parameter is None:
                return await self.get_settings(is_json=False)
            values[tag] = getattr(parameter, 'default_value', None)
            await self.logic.settings_redact(values)
        else:
            await self.logic.settings_default(parametr=tag, is_all=is_all)
        await self.callback.answer('⚙️ Настройка сброшена' if tag else '⚙️ Настройки сброшены')
        return await self.get_settings()

    async def edit_setting(self, tag: str):
        data = await self.logic.settings_detail()
        values = values_by_tag(data.settings.groups)
        parameter = next((
            parameter
            for group in data.settings.groups
            for parameter in group.parametrs
            if parameter.tag == tag and is_setting_available(parameter, values)
        ), None)
        if parameter is None or parameter.is_hidden or not parameter.is_redact:
            return await self.get_settings(is_json=False)
        if parameter.subparameters:
            return await self.setting_subparameters(tag)
        if isinstance(parameter.value, bool):
            values[tag] = not parameter.value
            await self.logic.settings_redact(values)
            return await self.get_settings(is_json=False)
        choices = getattr(parameter, 'choises', None)
        options = list(choices) if isinstance(choices, dict) else list(parameter.allowed_values or [])
        if options:
            current_index = options.index(parameter.value) if parameter.value in options else -1
            values[tag] = options[(current_index + 1) % len(options)]
            await self.logic.settings_redact(values)
            return await self.get_settings(is_json=False)

        await self.fsm.set_state(OrganState.setting_text)
        await self.fsm.update_data(setting_tag=tag)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([AnswerBody(
            text=f'✒️ Введите новое значение для «{parameter.name}»',
            reply_markup=self.IKB.settings_text_prompt(tag, not parameter.is_default_value),
        )])

    async def redact_setting_text(self):
        tag = await self.fsm.get_value('setting_tag')
        if not tag:
            await self.fsm.set_state()
            return await self.get_settings(is_json=False)
        data = await self.logic.settings_detail()
        values = values_by_tag(data.settings.groups)
        parameter = next((
            parameter
            for group in data.settings.groups
            for parameter in group.parametrs
            if parameter.tag == tag
        ), None)
        if parameter is None:
            await self.fsm.set_state()
            return await self.get_settings(is_json=False)
        try:
            value = coerce_setting_input(self.message.text or '', parameter)
        except ValueError as error:
            await self.answer([AnswerBody(
                text=f'⚠️ {error}',
                reply_markup=self.IKB.settings_text_prompt(tag, not parameter.is_default_value),
            )])
            return False
        values[tag] = value
        await self.logic.settings_redact(values)
        msg0 = await self.fsm.get_message()
        await self.fsm.set_state()
        if all(msg0):
            await self.bot.delete_message(*msg0)
        await self.fsm.remove_value('setting_tag')
        await self.fsm.remove_message()
        return await self.get_settings(is_json=False)

    async def to_redact_settings(self):
        await self.fsm.set_state(OrganState.settings)
        await self.fsm.update_data(organ_settings_json=True)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_enter_paramet(),
                reply_markup=self.IKB.settings_json(self.is_bot_message),
            )
        ])

    async def redact_settings(self):
        try:
            values = json5.loads(self.message.text)
            if not isinstance(values, dict):
                raise TypeError('Ожидается JSON-объект')
            data = await self.logic.settings_detail()
            current_values = values_by_tag(data.settings.groups)
            new_values = current_values | values
            parameters = {
                parameter.tag: parameter
                for group in data.settings.groups
                for parameter in group.parametrs
            }
            unavailable = [
                parameters[tag].name
                for tag, value in values.items()
                if tag in parameters
                and value != current_values.get(tag)
                and not is_setting_available(parameters[tag], new_values)
            ]
            if unavailable:
                names = ', '.join(unavailable)
                await self.answer([AnswerBody(
                    text=f'⚠️ Нельзя изменить настройки, пока не выполнены их зависимости: {names}. Проверьте зависимые параметры и отправьте JSON ещё раз.',
                    reply_markup=self.IKB.settings_json(self.is_bot_message),
                )])
                return False
            await self.logic.settings_redact(new_values)
        except (json.JSONDecodeError, TypeError) as error:
            raise JSONEnterError(
                'Ввел невалидный json',
                json=self.message.text,
            ) from error
        return await self.get_settings()

    async def capture(self):
        data = await self.logic.capture()
        return await self.answer([
            AnswerBody(
                text=self.text(data).capture,
                data=data,
                reply_markup=(self.IKB.organ_back(data.organ.id) if self.is_bot_message else None),
            )
        ])

    async def uprank( self, purpose_tg_id: int, rank: int | None = None):
        data = await self.logic.uprank(purpose_tg_id=purpose_tg_id, rank=rank)
        return await self.answer([
            AnswerBody(
                text=self.text(data).uprank(data.new_rank),
                data=data,
                reply_markup=(self.IKB.member_back(purpose_tg_id) if self.is_bot_message else None),
            )
        ])

    async def downrank( self, purpose_tg_id: int, rank: int | None = None):
        data = await self.logic.downrank(purpose_tg_id=purpose_tg_id, rank=rank)
        return await self.answer([
            AnswerBody(
                text=self.text(data).downrank(data.new_rank),
                data=data,
                reply_markup=(self.IKB.member_back(purpose_tg_id) if self.is_bot_message else None),
            )
        ])

    async def kick(self, purpose_tg_id: int | None = None):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        data = await self.logic.member(purpose_tg_id=target_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.kick(data),
                data=data,
                reply_markup=self.IKB.kick(data, self.is_bot_message),
            )
        ])

    async def accert_kick(self, purpose_tg_id: int):
        data = await self.logic.kick(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).accert_kick,
                data=data,
                reply_markup=self.IKB.back(OrganBackValues.members),
            )
        ])

    async def cancel_kick(self):
        data = await self.logic.member()
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_kick,
                data=data,
            )
        ])

    async def titul(
        self,
        purpose_tg_id: int,
        titul: str | None = None
    ):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        member = await self.logic.member(self.tg_id)
        if not member.for_buttons.is_redact_titul:
            raise OrganPermissioError()
        if not titul:
            return await self.to_titul_redact(target_tg_id)
        return await self.titul_redact(titul=titul, purpose_tg_id=purpose_tg_id)

    async def to_titul_redact(self, purpose_tg_id: int | None = None):
        target_tg_id = await self.fsm.get_value('purpose_tg_id', purpose_tg_id if purpose_tg_id is not None else self.tg_id)
        await self.fsm.set_state(OrganState.titul)
        await self.fsm.update_data(purpose_tg_id=target_tg_id)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.redact_titul(),
                reply_markup=self.IKB.redact_titul(target_tg_id, self.is_bot_message),
            )
        ])

    async def titul_redact(self, titul: str | None = None, purpose_tg_id: int | None = None):
        target_tg_id = await self.fsm.get_value('purpose_tg_id', purpose_tg_id if purpose_tg_id is not None else self.tg_id)
        data = await self.logic.titul_redact(target_tg_id, titul or self.message.text)
        await self.fsm.remove_value('purpose_tg_id')
        return await self.answer([
            AnswerBody(
                text=self.text(data).titul(data.old_titul, data.new_titul),
                data=data,
                reply_markup=self.IKB.member_back(target_tg_id),
            )
        ])

    async def titul_delete(self, purpose_tg_id: int | None = None):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        data = await self.logic.titul_delete(purpose_tg_id=target_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).titul(data.old_titul, data.new_titul),
                data=data,
                reply_markup=self.IKB.member_back(target_tg_id),
            )
        ])

    async def to_give(self, purpose_tg_id: int | None = None):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        data = await self.logic.member(purpose_tg_id=target_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_give(data),
                data=data,
                reply_markup=self.IKB.give(target_tg_id, self.is_bot_message),
            )
        ])

    async def give(self, purpose_tg_id: int):
        data = await self.logic.give(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.give(data),
                data=data,
                reply_markup=self.IKB.member_back(purpose_tg_id),
            )
        ])

    async def cancel_give(self):
        data = await self.logic.info()
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_give,
                data=data,
            )
        ])
