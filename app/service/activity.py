from app.exception.base import PermissionError
from app.logic.activity import ActivityLogic
from app.logic.tracker import tracker
from app.service.base import AnswerBody, BaseService
from app.tg.text.activity import ActivityText

class ActivityService(BaseService):
    logic_class: type[ActivityLogic] = ActivityLogic
    logic: ActivityLogic
    text_class: type[ActivityText] = ActivityText
    text: type[ActivityText]

    async def activity(self):
        try:
            if await self.bot.get_chat_member_count(self.message.chat.id) <= 100:
                return
    
            if self.message.from_user is None or self.message.forward_origin is not None:
                return
    
            await tracker.check(self.tg_id, self.message.text)
            activity_count = await tracker.message_per_request(self.tg_id)
    
            data = await self.logic.activity(activity_count)
            return await self.answer([
                AnswerBody(
                    text=self.text.activity(data.get_activity_points),
                    data=data,
                    is_ephemeral=True,
                )
            ])
        except Exception as e:
            self.botlog.logger.trace(e)
            return

    async def activity_reset(self, purpose_tg_id: int | None = None):
        if not self.is_admin:
            raise PermissionError()
        target_tg_id = purpose_tg_id or self.purpose_tg_id or self.tg_id
        data = await self.logic.activity_reset(target_tg_id)
        return await self.answer([AnswerBody(text=self.text.limit_reset(data))])