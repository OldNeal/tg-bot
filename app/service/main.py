from aiogram.filters import CommandObject

from app.exception.base import PermissionError
from app.exception.args import UserSearchIdError, UserSearchValueError
from app.service.base import BaseService, AnswerBody
from app.logic.main import MainLogic
from app.tg.text.main import MainText
from app.tg.buttons.main import MainIKB
from app.tg.fsm.state import MainState
from app.tg.fsm.utils import MainFSM
from app.validate.api import AnswerUsersBody

class MainService(BaseService):
    logic_class: type[MainLogic] = MainLogic
    logic: MainLogic
    text_class: type[MainText] = MainText
    text: type[MainText]
    ikb_class: type[MainIKB] = MainIKB
    IKB: MainIKB
    fsm_class: type[MainFSM] = MainFSM
    fsm: MainFSM

    async def menu(self):
        return await self.answer([
            AnswerBody(
                text=self.text.menu(),
                reply_markup=self.IKB.menu(),
            )
        ])

    async def info(self, purpose_tg_id: int | None = None):
        data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).info,
                data=data,
                reply_markup=self.IKB.info(data)
            )
        ])

    async def ping(self):
        api_ping = await self.logic.test_api_connect()
        return await self.answer([
            AnswerBody(text=self.text.check_ping(api_ping), is_rich_text=True)
        ])

    async def my_state(self):
        data = await self.fsm.get_data()
        return await self.answer([
            AnswerBody(
                text=self.text.json(data),
                data=None,
                reply_markup=self.IKB.my_state(),
                is_rich_text=True,
            )
        ])

    async def my_state_clear(self):
        data = await self.fsm.clear()
        return await self.answer([
            AnswerBody(
                text=self.text.state_clear(),
                data=None,
                is_rich_text=True,
            )
        ])

    async def my_state_pop(self, command: CommandObject):
        data = await self.fsm.get_data()
        key = command.args
        if key in data:
            data.pop(key)
            await self.fsm.set_data(data)
            text = self.text.state_pop()
        else:
            text = self.text.state_dont_pop()
        return await self.answer([
            AnswerBody(text=text, data=None, is_rich_text=True)
        ])

    async def users(self, page: int | None = None, notice: str | None = None):
        await self.fsm.set_state()
        await self.fsm.remove_value('search')
        data = await self.logic.users_list(page=page or 0)
        return await self.show_users(data, notice=notice)

    async def users_search_fields(self):
        await self.fsm.set_state()
        return await self.answer([
            AnswerBody(
                text=self.text.users_search_fields(),
                reply_markup=self.IKB.users_search_fields(),
            )
        ])

    async def to_users_search(self, field: str):
        if field not in self.IKB.search_fields:
            return await self.users_search_fields()
        await self.fsm.set_state(MainState.users_search)
        await self.fsm.update_data(search_field=field)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.users_search_input(field),
                reply_markup=self.IKB.back_to_list(),
            )
        ])

    async def search_users(self):
        field = await self.fsm.get_value('search_field')
        if field not in self.IKB.search_fields:
            await self.fsm.set_state()
            return await self.users_search_fields()

        value = (self.message.text or '').strip()
        if not value:
            raise UserSearchValueError()
        if field in ('user_id', 'tg_id'):
            try:
                parsed_value = int(value)
            except ValueError:
                raise UserSearchIdError() from None
            if parsed_value <= 0:
                raise UserSearchIdError()
        else:
            parsed_value = value.removeprefix('@') if field == 'username' else value
            if not parsed_value:
                raise UserSearchValueError()

        criteria = {field: parsed_value}
        data = await self.logic.users_search(page=0, **criteria)
        await self.fsm.update_data(search=criteria, page=data.page.number)
        await self.fsm.set_state()
        saved_message = await self.fsm.get_message()
        if saved_message[0] and saved_message[1]:
            await self.bot.delete_message(*saved_message)
        await self.fsm.remove_message()
        return await self.show_users(data, is_search=True)

    async def users_page(self, page: int):
        criteria = await self.fsm.get_value('search')
        if criteria:
            data = await self.logic.users_search(page=page, **criteria)
            return await self.show_users(data, is_search=True)
        data = await self.logic.users_list(page=page)
        return await self.show_users(data)

    async def show_users(
        self,
        data: AnswerUsersBody,
        is_search: bool = False,
        notice: str | None = None,
    ):  
        current_page = data.users
        max_page = data.page.max
        page = data.page.number
        count = data.count
        await self.fsm.update_data(page=page)
        if is_search:
            text = self.text.users_search_results(count, page, max_page)
        else:
            text = self.text.users_list(count, page, max_page)
        if notice:
            text = f'{notice}\n\n{text}'
        print(data, len(data.users))
        return await self.answer([
            AnswerBody(
                text=text,
                data=data,
                reply_markup=self.IKB.users(current_page, page, max_page),
            )
        ])

    async def confirm_user_delete(self, user_id: int):
        data = await self.logic.user_info(user_id=user_id)
        return await self.answer([
            AnswerBody(
                text=self.text.user_delete_confirm(data.purpose),
                data=data,
                reply_markup=self.IKB.confirm_user_delete(user_id),
            )
        ])

    async def user_info(self, user_id: int | None = None):
        data = await self.logic.user_info(user_id if not user_id is None else await self.logic.user_id)
        return await self.answer([
            AnswerBody(
                text=self.text.user_info(data.purpose),
                data=data,
                reply_markup=self.IKB.user_info(data)
            )
        ])

    async def delete_user(self, user_id: int | None = None, confirmed: bool = False):
        my_user_id = await self.logic.user_id
        if user_id is None:
            user_id = my_user_id
        if user_id != my_user_id and not self.is_admin:
            raise PermissionError()
        if not confirmed:
            return await self.user_info(user_id)

        user = await self.logic.user_delete(user_id)
        criteria = await self.fsm.get_value('search')
        data = (
            await self.logic.users_search(**criteria)
            if criteria else await self.logic.users_list()
        )

        return await self.answer([
            AnswerBody(
                text=self.text.user_deleted(user),
                data=data,
                reply_markup=self.IKB.back('main'),
            )
        ])