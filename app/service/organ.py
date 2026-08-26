from app.service.base import BaseService
from app.logic.organ import OrganLogic
from app.validate.args import UserArg, OrganIdArg, SearchArg, InfoOrganIdArg, RankRedactArg, TitulRedactArg, NameArg, SettingRedactArg
from app.aio.cls.msg.organ import OrganText
from typing import TypeVar
from app.aio.cls.fsm.state import OrganState
from app.aio.cls.buttons.organ import OrganIKB
import json
from app.exception.base import JSONEnterError
from app.aio.cls.fsm.utils import OrganFSM
from app.aio.cls.callback.back import OrganBackValues

ARG = TypeVar('ARG', bound=UserArg)

class OrganService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = OrganLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = OrganText
        self.IKB = OrganIKB(self.tg_id)
        self.state = OrganFSM(state)

    async def menu(self):
        data = await self.logic.member()
        return self.to_json([
            [self.text.menu(), data, self.IKB.menu()]
            ])
    
    async def member(self, purpose_tg_id: int | None = None):
        await self.state.set_state()
        if purpose_tg_id:
            data = await self.logic.member(purpose_tg_id)
        else:
            data = await self.logic.member(**UserArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text.member(data), data, self.IKB.member(data)]
            ])

    async def info(self, organ_id: int | None = None, purpose_tg_id: int | None = None, is_back: bool = False):
        back_where2 = await self.state.get_value('back_where2')
        if organ_id is None and purpose_tg_id is None and not is_back:
            data = await self.logic.info(**InfoOrganIdArg.model_validate(self.kwargs).model_dump())
        elif is_back:
            organ_id = await self.state.get_value('organ_id')
            data = await self.logic.info(organ_id=organ_id)
        else:
            data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        await self.state.update_data(back_where=OrganBackValues.info)
        return self.to_json([
            [self.text(data).info, data, self.IKB.info(data, where=back_where2)]
            ])

    async def search(self, value: str | None = None, is_back: bool = False, page: int | None = None):
        page = page if not(page is None) else await self.state.get_value('page', 0)
        value = await self.state.get_value('search_value', value)
        args = SearchArg.model_validate(self.kwargs)
        if is_back and value:
            data = await self.logic.search(value=value)
        elif args.value:
            data = await self.logic.search(**args.model_dump())
        else:
            return await self.to_enter_search()
        organ_ids = {o.id:o for o in data.organs}
        pages = self.to_pages([o.id for o in data.organs])
        max_page = len(pages)
        if len(data.organs) == 0:
            await self.state.update_data(back_where2=OrganBackValues.search, pages=pages, page=page)
        else:
            await self.state.update_data(search_value=data.search_value, back_where2=OrganBackValues.search, pages=pages, page=page)
        return self.to_json([
            [self.text.search(data.search_value, len(data.organs), page, max_page), data, self.IKB.organs(([organ_ids.get(organ_id) for organ_id in pages[page]] if len(pages) > 0 else []), page, max_page, OrganBackValues.search)]
            ])

    async def to_enter_search(self):
        await self.state.set_state(OrganState.search)
        await self.state.update_data(msg=self.message)
        return self.to_json([
            [self.text.to_search(), None, self.IKB.cancel()]
            ])

    async def to_search(self):
        return await self.search(self.message.text, is_back=True)

    async def info_members(self, organ_id: int | None = None):
        if organ_id:
            data = await self.logic.info_members(organ_id=organ_id)
        else:
            data = await self.logic.info_members(**InfoOrganIdArg.model_validate(self.kwargs).model_dump())
        await self.state.update_data(organ_id=data.id)
        return self.to_json([
            [self.text(data).members, data, self.IKB.members(data.members, data.id)]
            ])
    
    async def info_description(self, organ_id: int | None = None):
        if organ_id:
            data = await self.logic.info_description(organ_id=organ_id)
        else:
            data = await self.logic.info_description(**InfoOrganIdArg.model_validate(self.kwargs).model_dump())
        await self.state.update_data(organ_id=data.id)
        return self.to_json([
            [self.text(data).desc, data, self.IKB.organ_back(data.id)]
            ])
    
    async def list(self, page: int | None = None):
        page = page if not(page is None) else await self.state.get_value('page', 0)
        data = await self.logic.list()
        organ_ids = {o.id:o for o in data.organs}
        pages = self.to_pages([o.id for o in data.organs])
        max_page = len(pages)
        await self.state.update_data(back_where2=OrganBackValues.list, pages=pages, page=page)
        return self.to_json([
            [self.text.list(page, max_page), data, self.IKB.organs([organ_ids.get(organ_id) for organ_id in pages[page]], page, max_page)]
            ])

    async def top(self):
        data = await self.logic.top_members()
        await self.state.update_data(back_where2=OrganBackValues.top)
        return self.to_json([
            [self.text.top(), data, self.IKB.top(data.organs)]
            ])

    

    
    async def login(self, organ_id: int | None = None):
        args = OrganIdArg(organ_id=organ_id) if organ_id else OrganIdArg.model_validate(self.kwargs)
        if args.organ_id:
            data = await self.logic.login(**args.model_dump())
            return self.to_json([
                [self.text(data).login, data, self.IKB.organ_back(data.organ.id)]
                ])
        else:
            return await self.search()
    
    async def to_exit(self):
        data = await self.logic.info()
        return self.to_json([
            [self.text.to_exit(), data, self.IKB.exit(data.organ.id)]
            ])
    
    async def exit(self):
        data = await self.logic.exit()
        return self.to_json([
            [self.text(data).exit, data, self.IKB.organ_back(data.organ.id)]
            ])

    async def cancel_exit(self):
        data = await self.logic.info()
        return self.to_json([
            [self.text(data).cancel_exit, data, None]
            ])

    async def create(self):
        data = await self.logic.create(**NameArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).create, data, None]
            ])
    
    async def get_settings(self):
        await self.state.set_state()
        data = await self.logic.settings()
        return self.to_json([
            [self.text(data).settings_values(data.values), data, self.IKB.settings_values(self.is_bot_message)]
            ])

    async def default_settings(self):
        await self.logic.settings_default(is_all=True)
        await self.callback.answer('⚙️ Настройки сброшены')
        return await self.get_settings()

    async def to_redact_settings(self):
        await self.state.set_state(OrganState.settings)
        await self.state.update_data(msg=self.message)
        return self.to_json([
            [self.text.to_enter_paramet(), None, self.IKB.back(OrganBackValues.search)]
            ])

    async def redact_settings(self):
        try:
            await self.logic.settings_redact(json.loads(self.message.text))
        except json.JSONDecodeError:
            raise JSONEnterError('Ввел невалидный json', json=self.message.text)
        return await self.get_settings()

    async def capture(self, organ_id: int | None = None):
        if organ_id:
            data = await self.logic.login(organ_id=organ_id)
        else:
            data = await self.logic.login(**OrganIdArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).capture, data, (self.IKB.organ_back(organ_id) if self.is_bot_message else None)]
            ])




    def check_enter_purpose(self, model: type[ARG]) -> ARG:
        args = model.model_validate(self.kwargs)
        if args.purpose_tg_id is None and self.purpose is None:
            raise
        return args
    
    async def uprank(self, purpose_tg_id: int | None = None, new_rank: int | None = None):
        if purpose_tg_id:
            data = await self.logic.uprank(purpose_tg_id, new_rank)
        else:
            data = await self.logic.uprank(**self.check_enter_purpose(RankRedactArg).model_dump())
        return self.to_json([
            [self.text(data).uprank(data.new_rank), data, (self.IKB.member_back(data.user.tg_id) if self.is_bot_message else None)]
            ])
    
    async def downrank(self, purpose_tg_id: int | None = None, new_rank: int | None = None):
        if purpose_tg_id:
            data = await self.logic.downrank(purpose_tg_id, new_rank)
        else:
            data = await self.logic.downrank(**self.check_enter_purpose(RankRedactArg).model_dump())
        return self.to_json([
            [self.text(data).downrank(data.new_rank), data, (self.IKB.member_back(data.user.tg_id) if self.is_bot_message else None)]
            ])
    
    async def kick(self, purpose_tg_id: int | None = None):
        if purpose_tg_id:
            data = await self.logic.member(purpose_tg_id)
        else:
            data = await self.logic.member(**self.check_enter_purpose(UserArg).model_dump())
        return self.to_json([
            [self.text.kick(data), data, self.IKB.kick(data, self.is_bot_message)]
            ])

    async def accert_kick(self, purpose_tg_id: int):
        data = await self.logic.kick(purpose_tg_id)
        return self.to_json([
            [self.text(data).accert_kick, data, self.IKB.back(OrganBackValues.members)]
            ])

    async def cancel_kick(self):
        data = await self.logic.member()
        return self.to_json([
            [self.text(data).cancel_kick, None, None]
            ])

    async def titul(self, purpose_tg_id: int | None = None):
        arg = self.check_enter_purpose(TitulRedactArg)
        if purpose_tg_id and not arg.titul:
            return await self.to_titul_redact(purpose_tg_id)
        else:
            return await self.titul_redact(**arg.model_dump())

    async def to_titul_redact(self, purpose_tg_id: int):
        await self.state.set_state(OrganState.titul)
        await self.state.update_data(msg=self.message, purpose_tg_id=purpose_tg_id)
        return self.to_json([
            [self.text.redact_titul(), None, self.IKB.redact_titul(purpose_tg_id, self.is_bot_message)]
            ])

    async def titul_redact(self, titul: str | None = None, purpose_tg_id: int | None = None):
        purpose_tg_id = await self.state.get_value('purpose_tg_id', purpose_tg_id)
        data = await self.logic.titul_redact(purpose_tg_id, titul or self.message.text)
        return self.to_json([
            [self.text(data).titul(data.old_titul, data.new_titul), data, self.IKB.member_back(purpose_tg_id)]
            ])

    async def titul_delete(self, purpose_tg_id: int | None = None):
        if purpose_tg_id:
            data = await self.logic.titul_delete(purpose_tg_id)
        else:
            data = await self.logic.titul_delete(**self.check_enter_purpose(UserArg).model_dump())
        return self.to_json([
            [self.text(data).titul(data.old_titul, data.new_titul), data, self.IKB.member_back(data.user.tg_id)]
            ])

    async def to_give(self, purpose_tg_id: int | None = None):
        if purpose_tg_id:
            data = await self.logic.member(purpose_tg_id)
        else:
            data = await self.logic.member(**self.check_enter_purpose(UserArg).model_dump())
        return self.to_json([
            [self.text.to_give(data), data, self.IKB.give(data.user.tg_id, self.is_bot_message)]
            ])
 
    async def give(self, purpose_tg_id: int):
        data = await self.logic.give(purpose_tg_id)
        return self.to_json([
            [self.text(data).give(), data, self.IKB.member_back(data.user.tg_id)]
            ])
 
    async def cancel_give(self):
        data = await self.logic.info()
        return self.to_json([
            [self.text(data).cancel_give, data, None]
            ])