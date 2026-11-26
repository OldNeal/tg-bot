from app.exception.base import PermissionError
from app.logic.activity import ActivityLogic
from app.logic.tracker import tracker
from app.service.base import AnswerBody, BaseService
from app.tg.text.activity import ActivityText
from app.tg.buttons.activity import ActivityIKB

class ActivityService(BaseService):
    logic_class: type[ActivityLogic] = ActivityLogic
    logic: ActivityLogic
    text_class: type[ActivityText] = ActivityText
    text: type[ActivityText]
    ikb_class: type[ActivityIKB] = ActivityIKB
    IKB: ActivityIKB

    async def activity(self):
        try:
            if await self.bot.get_chat_member_count(self.message.chat.id) < 50:
                return
    
            if self.message.from_user is None or self.message.forward_origin is not None:
                return
    
            await tracker.check(self.tg_id, self.message.text)
            activity_count = await tracker.message_per_request(self.tg_id)
    
            data = await self.logic.activity(activity_count)
            if data.user.setting.get_notify and (data.user.setting.is_send_to_private or data.user.setting.is_ephemeral):
                return await self.answer([
                    AnswerBody(
                        text=self.text.activity(data.get_activity_points),
                        data=data,
                        reply_markup=self.IKB.delete_notify(),
                        is_send_to_private=data.user.setting.is_send_to_private,
                        is_ephemeral=data.user.setting.is_ephemeral
                    )
                ])
        except Exception as e:
            self.botlog.logger.trace(e)
            return

    async def limits(
        self, 
        item_id: int,
        source: str,
        page: int
    ):
        data = await self.logic.limits()
        return await self.answer([
                AnswerBody(
                    text=self.text.limits(data),
                    data=data,
                    reply_markup=self.IKB.back_to_items(item_id, source, page),
                    is_ephemeral=True,
                )
            ])


    async def activity_reset(self, purpose_tg_id: int | None = None):
        if not self.is_admin:
            raise PermissionError()
        target_tg_id = purpose_tg_id or self.purpose_tg_id or self.tg_id
        data = await self.logic.activity_reset(target_tg_id)
        return await self.answer([AnswerBody(text=self.text.limit_reset(data))])