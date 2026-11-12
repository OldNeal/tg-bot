from app.exception.activity import ActivityUnknownActionError, ActivityEnterPointsError
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

    async def ap(
        self,
        action: str,
        purpose_tg_id: int | None = None,
        points: int | None = None,
        reason: str | None = None
    ):
        if not self.is_admin:
            raise PermissionError()
        target_tg_id = purpose_tg_id or self.purpose_tg_id or self.tg_id
        if action in ('add', 'deduct') and points is None:
            raise ActivityEnterPointsError()
        if action == 'add':
            return await self.add_points(target_tg_id, points, reason)
        elif action == 'deduct':
            return await self.deduct_points(target_tg_id, points, reason)
        elif action == 'reset':
            return await self.reset_points(target_tg_id, reason)
        elif action == 'limit_reset':
            return await self.reset_limit(target_tg_id)
        else:
            raise ActivityUnknownActionError()

    async def add_points(
        self,
        purpose_tg_id: int,
        points: int,
        reason: str | None = None,
    ):
        data = await self.logic.add_points(purpose_tg_id, points, reason)
        return await self.answer([AnswerBody(text=self.text.added(data))])

    async def deduct_points(
        self,
        purpose_tg_id: int,
        points: int,
        reason: str | None = None,
    ):
        data = await self.logic.deduct_points(purpose_tg_id, points, reason)
        return await self.answer([AnswerBody(text=self.text.deducted(data))])

    async def reset_points(self, purpose_tg_id: int, reason: str | None = None):
        data = await self.logic.reset_points(purpose_tg_id, reason)
        return await self.answer([AnswerBody(text=self.text.reset(data))])

    async def reset_limit(self, purpose_tg_id: int):
        data = await self.logic.reset_limit(purpose_tg_id)
        return await self.answer([AnswerBody(text=self.text.limit_reset(data))])