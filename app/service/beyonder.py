from datetime import datetime, timedelta

from app.service.base import BaseService, AnswerBody
from app.logic.beyonder import BeyonderLogic
from app.validate.text import RedactSeqTextValidate, UserTextValidate
from app.tg.text.beyonder import BeyonderText
from app.tg.buttons.beyonder import BeyonderIKB
from app.tg.callback.back_values import BeyonderBackValues
from app.tg.callback.wiki import WikiSearchCall
from app.tg.fsm.utils import BeyonderFSM

class BeyonderService(BaseService):
    logic_class: type[BeyonderLogic] = BeyonderLogic
    logic: BeyonderLogic
    text_class: type[BeyonderText] = BeyonderText
    text: type[BeyonderText]
    ikb_class: type[BeyonderIKB] = BeyonderIKB
    IKB: BeyonderIKB
    fsm_class: type[BeyonderFSM] = BeyonderFSM
    fsm: BeyonderFSM

    async def info(self, purpose_tg_id: int | None = None):
        back_where = await self.fsm.get_value('back_where')
        data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        reply_markup = self.IKB.info_card(data, where=back_where) if data.purpose and data.purpose.telegram else None
        if back_where and reply_markup is None:
            reply_markup = self.IKB.back(back_where)
        return await self.answer([
            AnswerBody(
                text=self.text(data).info,
                data=data,
                reply_markup=reply_markup
            )
        ])

    async def drink(
        self,
        path_id: int | None = None,
        path_name: str | None = None,
        seq: int = 9,
        purpose_tg_id: int | None = None
    ):
        if path_id:
            data = await self.logic.drink(path_id=path_id)
        else:
            if path_name is None:
                return await self.answer([
                    AnswerBody(
                        text='Путь не указан. Нажмите кнопку ниже, чтобы найти его.',
                        reply_markup=self.IKB.builder.button(
                            text='🔍 Найти путь',
                            callback_data=WikiSearchCall(type='path', tg_id=self.tg_id),
                        ).as_markup(),
                    )
                ])
            data = await self.logic.drink(purpose_tg_id=purpose_tg_id, path_name=path_name, seq=seq)
        return await self.answer([
            AnswerBody(
                text=self.text(
                    RedactSeqTextValidate(
                        seq_name=data.new.seq,
                        path_name=data.new.path,
                        name=self.text.answer_user_name(data.purpose)
                    )
                ).drink,
                data=data
            )
        ])

    async def upseq(
        self,
        seq: int | None = None,
        path_name: str | None = None,
        path_id: int | None = None,
        purpose_tg_id: int | None = None,
    ):
        info = await self.logic.time_info(purpose_tg_id=purpose_tg_id, to_raise=True)
        if path_id is not None:
            path = await self.logic.path(id=path_id)
        else:
            current_path_name = path_name or info.beyonder.path_name
            path = await self.logic.path(name=current_path_name)
        ga = await self.logic.ga(id=path.ga.ga_id)
        paths = ga.paths
        if not any(item.path_id == path.path_id for item in paths):
            paths = [*paths, path]
        return await self.answer([
            AnswerBody(
                text=(
                    f'🚀 Подтвердите продвижение {self.text.user_mention(info.purpose)} '
                    f'по пути «{path.name}»'
                    + (f' до последовательности {seq}' if seq is not None else '')
                ),
                data=info,
                reply_markup=self.IKB.confirm_upseq(
                    paths,
                    path.path_id,
                    info.purpose.telegram.tg_id
                    if info.purpose and info.purpose.telegram
                    else purpose_tg_id or self.purpose.id,
                    seq,
                ),
            )
        ])

    async def confirm_upseq(self, seq: int | None = None, path_id: int | None = None, purpose_tg_id: int | None = None):
        path = await self.logic.path(id=path_id) if path_id is not None else None
        data = await self.logic.upseq(
            purpose_tg_id=purpose_tg_id,
            path_name=path.name if path else None,
            seq=seq,
        )
        return await self.answer([
            AnswerBody(
                text=self.text(
                    RedactSeqTextValidate(
                        seq_name=data.new.seq,
                        path_name=data.new.path,
                        name=self.text.answer_user_name(data.purpose)
                    )
                ).upseq,
                data=data
            )
        ])

    async def cancel_upseq(self):
        return await self.answer([
            AnswerBody(text='❌ Продвижение отменено.')
        ])

    async def dowseq(self, seq: int | None = None, path_name: str | None = None, purpose_tg_id: int | None = None):
        data = await self.logic.dowseq(purpose_tg_id=purpose_tg_id, path_name=path_name, seq=seq)
        return await self.answer([
            AnswerBody(
                text=self.text(
                    RedactSeqTextValidate(
                        seq_name=data.new.seq,
                        path_name=data.new.path,
                        name=self.text.answer_user_name(data.purpose)
                    )
                ).downseq,
                data=data
            )
        ])

    async def kill(self, purpose_tg_id: int | None = None, is_admin: bool = False):
        data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).kill(
                    self.tg_id,
                    is_admin=is_admin and self.tg_id_in_admins
                ),
                data=data,
                reply_markup=self.IKB.accert_kill(purpose_tg_id or self.purpose.id)
            )
        ])

    async def accert_kill(self, purpose_tg_id: int):
        data = await self.logic.kill(
            purpose_tg_id=purpose_tg_id,
            is_admin=self.tg_id_in_admins
        )
        return await self.answer([
            AnswerBody(
                text=self.text(UserTextValidate(name=self.text.answer_user_name(data.purpose))).accert_kill,
                data=data
            )
        ])

    async def cancel_kill(self, purpose_tg_id: int):
        data = await self.logic.info(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).cancel_kill,
                data=data
            )
        ])

    async def time_info(self, purpose_tg_id: int | None = None):
        data = await self.logic.time_info(purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).time_info,
                data=data,
                reply_markup=self.IKB.back_to_card(purpose_tg_id) if not purpose_tg_id is None else None
            )
        ])

    async def time_redact(self, duration: timedelta, purpose_tg_id: int | None = None):
        data = await self.logic.time_redact(duration=duration, purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).time_redact,
                data=data
            )
        ])

    async def time_replace(self, datetime_arg: datetime, purpose_tg_id: int | None = None):
        data = await self.logic.time_replace(datetime_arg=datetime_arg, purpose_tg_id=purpose_tg_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).time_replace,
                data=data
            )
        ])

    async def list(self, path_id: int | None = None, page: int | None = None, where: str | None = None):
        page = page if page is not None else await self.fsm.get_value('page', 0)
        path_id = path_id if path_id is not None else await self.fsm.get_value('path_id')
        data = await self.logic.list(path_id)
        if data.ga:
            data.beyonders = [data.ga] + data.beyonders
        pages = self.to_pages(data.beyonders)
        max_page = len(pages)
        if page >= max_page:
            page = 0
        await self.fsm.update_data(back_where=BeyonderBackValues.list, page=page, path_id=path_id)
        return await self.answer([
            AnswerBody(
                text=self.text(data).list(max_page, page),
                data=data,
                reply_markup=self.IKB.list(
                    pages[page] if pages else [],
                    page,
                    max_page,
                    data.path.path_id,
                    where=where
                )
            )
        ])
