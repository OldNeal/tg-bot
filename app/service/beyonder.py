from app.service.base import BaseService
from app.logic.beyonder import BeyonderLogic
from app.validate.args import UserArg, DrinkArg, UpDownSeqArg, TimeReplaceArg, TimeRedactArg
from app.aio.cls.msg.beyonder import BeyonderText
from app.validate.text import RedactSeqTextValidate, UserTextValidate

class BeyonderService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = BeyonderLogic(tg_id=self.tg_id, username=self.user.username, fullname=self.user.full_name, **self.logic_kwargs)
        self.text = BeyonderText

    async def drink(self):
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
        data = await self.logic.kill(**UserArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(UserTextValidate(name=data.user.fullname)).kill, data, None]
            ])

    async def time_info(self):
        data = await self.logic.time_info(**UserArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [self.text(data).time_info, data, None]
            ])

    async def time_redact(self):
        data = await self.logic.time_redact(**TimeRedactArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [data.model_dump_json(), data, None]
            ])
    
    async def time_replace(self):
        data = await self.logic.time_replace(**TimeReplaceArg.model_validate(self.kwargs).model_dump())
        return self.to_json([
            [data.model_dump_json(), data, None]
            ])
    