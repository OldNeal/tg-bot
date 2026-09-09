from app.service.base import BaseService
from app.logic.beyonder import BeyonderLogic
from app.validate.args import UserArg, DrinkArg, UpDownSeqArg, TimeReplaceArg, TimeRedactArg
from app.aio.cls.msg.beyonder import BeyonderText
from app.validate.text import RedactSeqTextValidate, UserTextValidate
from app.aio.cls.buttons.beyonder import BeyonderIKB

class BeyonderService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = BeyonderLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = BeyonderText
        self.IKB = BeyonderIKB(self.tg_id)

    async def drink(self, path_id: int | None = None):
        if path_id:
            data = await self.logic.drink(path_id=path_id)
        else:
            data = await self.logic.drink(**DrinkArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(RedactSeqTextValidate(seq_name=data.new.seq, path_name=data.new.path, name=data.user.fullname)).drink, data, None]
            ])

    async def upseq(self):
        data = await self.logic.upseq(**UpDownSeqArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(RedactSeqTextValidate(seq_name=data.new.seq, path_name=data.new.path, name=data.user.fullname)).upseq, data, None]
            ])

    async def dowseq(self):
        data = await self.logic.dowseq(**UpDownSeqArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(RedactSeqTextValidate(seq_name=data.new.seq, path_name=data.new.path, name=data.user.fullname)).downseq, data, None]
            ])

    async def kill(self):
        data = await self.logic.info(**UserArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).kill(self.tg_id, is_admin=self.is_admin), data, self.IKB.accert_kill(data.user.tg_id)]
            ])

    async def accert_kill(self, purpose_tg_id: int):
        data = await self.logic.redact_kwargs(is_admin=self.tg_id_in_admins).kill(purpose_tg_id=purpose_tg_id)
        return self.to_json([
            [self.text(UserTextValidate(name=data.user.fullname)).accert_kill, data, None]
            ])

    async def cancel_kill(self, purpose_tg_id: int):
        data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        return self.to_json([
            [self.text(data).cancel_kill, data, None]
            ])


    async def time_info(self):
        data = await self.logic.time_info(**UserArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).time_info, data, None]
            ])

    async def time_redact(self):
        data = await self.logic.time_redact(**TimeRedactArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).time_redact, data, None]
            ])
    
    async def time_replace(self):
        data = await self.logic.time_replace(**TimeReplaceArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).time_replace, data, None]
            ])
    