import json, json5

from app.service.base import BaseService, AnswerBody
from app.logic.organ import OrganLogic
from app.validate.args import (
    InfoOrganIdArg,
    NameArg,
    OrganIdArg,
    RankRedactArg,
    TitulRedactArg,
    UserArg,
)
from app.tg.text.organ import OrganText
from app.tg.buttons.organ import OrganIKB
from app.tg.fsm.state import OrganState
from app.tg.fsm.utils import OrganFSM
from app.tg.callback.back_values import OrganBackValues
from app.exception.organ import OrganPermissioError
from app.exception.base import JSONEnterError

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
        await self.fsm.remove_value('back_where2')
        return await self.answer([
            AnswerBody(
                text=self.text.menu(),
                reply_markup=self.IKB.menu(),
                is_rich_text=True,
            )
        ])

    async def my_organ(self):
        try:
            return await self.info()
        except Exception:
            return await self.answer([
                AnswerBody(
                    text=self.text.my_organ(),
                    reply_markup=self.IKB.my_organ(),
                    is_rich_text=True,
                )
            ])

    async def member(self, purpose_tg_id: int | None = None):
        await self.fsm.set_state()
        if purpose_tg_id:
            data = await self.logic.member(purpose_tg_id)
        else:
            data = await self.logic.member(
                **UserArg(purpose_tg_id=self.purpose.id).model_dump()
            )
        return await self.answer([
            AnswerBody(
                text=self.text.member(data),
                data=data,
                reply_markup=self.IKB.member(data),
                is_rich_text=True,
            )
        ])

    async def info(
        self,
        organ_id: int | None = None,
        purpose_tg_id: int | None = None,
        is_back: bool = False,
    ):
        back_where2 = await self.fsm.pop_value('back_where2')
        if organ_id is None and purpose_tg_id is None and not is_back:
            data = await self.logic.info(
                **InfoOrganIdArg(organ_id=organ_id).model_dump()
            )
        elif is_back:
            organ_id = await self.fsm.get_value('organ_id')
            data = await self.logic.info(organ_id=organ_id)
        else:
            data = await self.logic.info(
                organ_id=organ_id,
                purpose_tg_id=purpose_tg_id,
            )
        return await self.answer([
            AnswerBody(
                text=self.text(data).info,
                data=data,
                reply_markup=self.IKB.info(data, where=back_where2),
                is_rich_text=True,
            )
        ])

    async def search(
        self,
        value: str | None = None,
        is_back: bool = False,
        page: int | None = None,
    ):
        page = page if page is not None else await self.fsm.get_value('page', 0)
        value = await self.fsm.get_value('search_value', value)
        if is_back and value:
            data = await self.logic.search(value=value)
        elif value:
            data = await self.logic.search(value=value)
        else:
            return await self.to_enter_search()

        pages = self.to_pages(data.organs)
        max_page = len(pages)
        if len(data.organs) == 0:
            await self.fsm.update_data(
                back_where2=OrganBackValues.search,
                page=page,
            )
        else:
            await self.fsm.update_data(
                search_value=data.search_value,
                back_where2=OrganBackValues.search,
                page=page,
            )
        current_page = pages[page if page < max_page else 0] if pages else []
        return await self.answer([
            AnswerBody(
                text=self.text.search(
                    data.search_value,
                    len(data.organs),
                    page,
                    max_page,
                ),
                data=data,
                reply_markup=self.IKB.organs(
                    current_page,
                    page,
                    max_page,
                    OrganBackValues.search,
                ),
                is_rich_text=True,
            )
        ])

    async def to_enter_search(self):
        await self.fsm.set_state(OrganState.search)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_search(),
                reply_markup=self.IKB.cancel(),
                is_rich_text=True,
            )
        ])

    async def to_search(self):
        return await self.search(self.message.text, is_back=True)

    async def enter_search(self):
        await self.fsm.remove_value('search_value')
        return await self.search()

    async def info_members(
        self,
        organ_id: int | None = None,
        page: int | None = None,
    ):
        page = (
            page
            if page is not None
            else await self.fsm.get_value('info_members_page', 0)
        )
        if organ_id:
            data = await self.logic.info_members(organ_id=organ_id)
        else:
            data = await self.logic.info_members(
                **InfoOrganIdArg(organ_id=organ_id).model_dump()
            )
        pages = self.to_pages(sorted(data.members, key=lambda x: x.member.rank))
        max_page = len(pages)
        await self.fsm.update_data(organ_id=data.id, info_members_page=page)
        current_page = pages[page if page < max_page else 0] if pages else []
        return await self.answer([
            AnswerBody(
                text=self.text(data).members(page, max_page),
                data=data,
                reply_markup=self.IKB.members(
                    current_page,
                    page,
                    max_page,
                    data.id,
                ),
                is_rich_text=True,
            )
        ])

    async def info_description(self, organ_id: int | None = None):
        if organ_id:
            data = await self.logic.info_description(organ_id=organ_id)
        else:
            data = await self.logic.info_description(
                **InfoOrganIdArg(organ_id=organ_id).model_dump()
            )
        await self.fsm.update_data(organ_id=data.id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).desc,
                data=data,
                reply_markup=self.IKB.organ_back(data.id),
                is_rich_text=True,
            )
        ])

    async def list(self, page: int | None = None):
        page = page if page is not None else await self.fsm.get_value('page', 0)
        data = await self.logic.list()
        pages = self.to_pages(data.organs)
        max_page = len(pages)
        await self.fsm.update_data(back_where2=OrganBackValues.list, page=page)
        current_page = pages[page if page < max_page else 0] if pages else []
        return await self.answer([
            AnswerBody(
                text=self.text.list(page, max_page),
                data=data,
                reply_markup=self.IKB.organs(current_page, page, max_page),
                is_rich_text=True,
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
                is_rich_text=True,
            )
        ])

    async def login(self, organ_id: int | None = None):
        args = OrganIdArg(organ_id=organ_id)
        if args.organ_id:
            data = await self.logic.login(organ_id=args.organ_id)
            return await self.answer([
                AnswerBody(
                    text=self.text(data).login,
                    data=data,
                    reply_markup=self.IKB.organ_back(data.organ.id),
                    is_rich_text=True,
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
                is_rich_text=True,
            )
        ])

    async def exit(self):
        data = await self.logic.exit()
        return await self.answer([
            AnswerBody(
                text=self.text(data).exit,
                data=data,
                reply_markup=self.IKB.organ_back(data.organ.id),
                is_rich_text=True,
            )
        ])

    async def cancel_exit(self):
        data = await self.logic.info()
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_exit,
                data=data,
                is_rich_text=True,
            )
        ])

    async def create(self, name: str | None = None):
        args = NameArg(name=name)
        if args.name:
            data = await self.logic.create(name=args.name)
            return await self.answer([
                AnswerBody(
                    text=self.text(data).create,
                    data=data,
                    reply_markup=self.IKB.create(data.organ.id),
                    is_rich_text=True,
                )
            ])
        return await self.to_enter_name_for_create()

    async def to_enter_name_for_create(self):
        try:
            await self.logic.info()
        except Exception:
            await self.fsm.set_state(OrganState.create)
            await self.fsm.save_message(
                self.message.chat.id,
                self.message.message_id,
            )
            return await self.answer([
                AnswerBody(
                    text=self.text.to_create(),
                    reply_markup=self.IKB.cancel(),
                    is_rich_text=True,
                )
            ])
        raise OrganPermissioError()

    async def enter_name_for_create(self):
        return await self.create(self.message.text)

    async def get_settings(self):
        await self.fsm.set_state()
        data = await self.logic.settings()
        return await self.answer([
            AnswerBody(
                text=self.text(data).settings_values(data.values),
                data=data,
                reply_markup=self.IKB.settings_values(self.is_bot_message),
                is_rich_text=True,
            )
        ])

    async def default_settings(self):
        await self.logic.settings_default(is_all=True)
        await self.callback.answer('⚙️ Настройки сброшены')
        return await self.get_settings()

    async def to_redact_settings(self):
        await self.fsm.set_state(OrganState.settings)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_enter_paramet(),
                reply_markup=self.IKB.back(OrganBackValues.settings),
                is_rich_text=True,
            )
        ])

    async def redact_settings(self):
        try:
            await self.logic.settings_redact(json5.loads(self.message.text))
        except json.JSONDecodeError as error:
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
                reply_markup=(
                    self.IKB.organ_back(data.organ.id)
                    if self.is_bot_message
                    else None
                ),
                is_rich_text=True,
            )
        ])

    async def uprank(
        self,
        purpose_tg_id: int | None = None,
        rank: int | None = None,
    ):
        args = self._rank_args(purpose_tg_id, rank)
        data = await self.logic.uprank(
            purpose_tg_id=args.purpose_tg_id,
            new_rank=args.rank,
        )
        return await self.answer([
            AnswerBody(
                text=self.text(data).uprank(data.new_rank),
                data=data,
                reply_markup=(
                    self.IKB.member_back(data.user.tg_id)
                    if self.is_bot_message
                    else None
                ),
                is_rich_text=True,
            )
        ])

    async def downrank(
        self,
        purpose_tg_id: int | None = None,
        rank: int | None = None,
    ):
        args = self._rank_args(purpose_tg_id, rank)
        data = await self.logic.downrank(
            purpose_tg_id=args.purpose_tg_id,
            new_rank=args.rank,
        )
        return await self.answer([
            AnswerBody(
                text=self.text(data).downrank(data.new_rank),
                data=data,
                reply_markup=(
                    self.IKB.member_back(data.user.tg_id)
                    if self.is_bot_message
                    else None
                ),
                is_rich_text=True,
            )
        ])

    def _rank_args(
        self,
        purpose_tg_id: int | None,
        rank: int | None,
    ) -> RankRedactArg:
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        return RankRedactArg(purpose_tg_id=target_tg_id, rank=rank)

    async def kick(self, purpose_tg_id: int | None = None):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        data = await self.logic.member(purpose_tg_id=target_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.kick(data),
                data=data,
                reply_markup=self.IKB.kick(data, self.is_bot_message),
                is_rich_text=True,
            )
        ])

    async def accert_kick(self, purpose_tg_id: int):
        data = await self.logic.kick(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).accert_kick,
                data=data,
                reply_markup=self.IKB.back(OrganBackValues.members),
                is_rich_text=True,
            )
        ])

    async def cancel_kick(self):
        data = await self.logic.member()
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_kick,
                data=data,
                is_rich_text=True,
            )
        ])

    async def titul(
        self,
        purpose_tg_id: int | None = None,
        titul: str | None = None,
    ):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        args = TitulRedactArg(purpose_tg_id=target_tg_id, titul=titul)
        member = await self.logic.member(self.tg_id)
        if not member.for_buttons.is_redact_titul:
            raise OrganPermissioError()
        if not args.titul:
            return await self.to_titul_redact(target_tg_id)
        return await self.titul_redact(
            titul=args.titul,
            purpose_tg_id=args.purpose_tg_id,
        )

    async def to_titul_redact(self, purpose_tg_id: int | None = None):
        target_tg_id = await self.fsm.get_value(
            'purpose_tg_id',
            purpose_tg_id if purpose_tg_id is not None else self.tg_id,
        )
        await self.fsm.set_state(OrganState.titul)
        await self.fsm.update_data(purpose_tg_id=target_tg_id)
        await self.fsm.save_message(self.message.chat.id, self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.redact_titul(),
                reply_markup=self.IKB.redact_titul(
                    target_tg_id,
                    self.is_bot_message,
                ),
                is_rich_text=True,
            )
        ])

    async def titul_redact(
        self,
        titul: str | None = None,
        purpose_tg_id: int | None = None,
    ):
        target_tg_id = await self.fsm.get_value(
            'purpose_tg_id',
            purpose_tg_id if purpose_tg_id is not None else self.tg_id,
        )
        data = await self.logic.titul_redact(
            target_tg_id,
            titul or self.message.text,
        )
        return await self.answer([
            AnswerBody(
                text=self.text(data).titul(data.old_titul, data.new_titul),
                data=data,
                reply_markup=self.IKB.member_back(target_tg_id),
                is_rich_text=True,
            )
        ])

    async def titul_delete(self, purpose_tg_id: int | None = None):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        data = await self.logic.titul_delete(purpose_tg_id=target_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).titul(data.old_titul, data.new_titul),
                data=data,
                reply_markup=self.IKB.member_back(data.user.tg_id),
                is_rich_text=True,
            )
        ])

    async def to_give(self, purpose_tg_id: int | None = None):
        target_tg_id = purpose_tg_id if purpose_tg_id is not None else self.purpose.id
        data = await self.logic.member(purpose_tg_id=target_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.to_give(data),
                data=data,
                reply_markup=self.IKB.give(data.user.tg_id, self.is_bot_message),
                is_rich_text=True,
            )
        ])

    async def give(self, purpose_tg_id: int):
        data = await self.logic.give(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text.give(data),
                data=data,
                reply_markup=self.IKB.member_back(data.user.tg_id),
                is_rich_text=True,
            )
        ])

    async def cancel_give(self):
        data = await self.logic.info()
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_give,
                data=data,
                is_rich_text=True,
            )
        ])
