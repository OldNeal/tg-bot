from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import bot, scheduler, settings
from app.logging.base import botlog
from app.redis.message import MessageStore
from app.redis.store import store
from app.tg.text.message import MessageText


class MessageSender:
    def __init__(
        self,
        bot: Bot = bot,
        message_store: MessageStore = store.message,
        scheduler: AsyncIOScheduler = scheduler,
    ):
        self.bot = bot
        self.store = message_store
        self.scheduler = scheduler
        self.settings = settings

    def start(self):
        self.scheduler.add_job(
            self.send_pending,
            trigger='interval',
            minutes=1,
            id='telegram_message_sender',
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

    def notification_enabled(self, key: str) -> bool:
        enabled_types = {
            self.store.hashs.GET_ACTIVITY_POINT: self.settings.telegram_notify_activity_points,
            self.store.hashs.item('give'): self.settings.telegram_notify_item_give,
            self.store.hashs.item('take'): self.settings.telegram_notify_item_take,
        }
        enabled_types.update({
            self.store.hashs.organ(action): self.settings.telegram_notify_organ
            for action in ('rank', 'titul', 'kick', 'give')
        })
        return self.settings.telegram_notifications_enabled and enabled_types.get(key, True)

    def notification_text(self, key: str, payload: dict[str, str]) -> str | None:
        if key == self.store.hashs.GET_ACTIVITY_POINT:
            return MessageText.activity_points(int(payload['points']), payload['reason'])
        for action in ('give', 'take'):
            if key == self.store.hashs.item(action):
                return MessageText.item(
                    action,
                    int(payload['item_id']),
                    int(payload['quantity']),
                    int(payload['remaining']),
                    item_name=payload.get('item_name'),
                    item_emodzi=payload.get('item_emodzi'),
                )
        for action in ('rank', 'titul', 'kick', 'give'):
            if key == self.store.hashs.organ(action):
                return MessageText.organ(action, payload)
        return None

    async def send_pending(self):
        if not self.settings.telegram_notifications_enabled:
            return
        async for key, payload in self.store.pending():
            try:
                if not self.notification_enabled(key):
                    continue
                text = self.notification_text(key, payload)
                if text is None:
                    botlog.logger.warning('Неизвестный тип Telegram-уведомления', key=key)
                    continue
                await self.bot.send_message(chat_id=int(payload['tg_id']), text=text)
                await self.store.delete_if_unchanged(key, payload)
            except Exception:
                botlog.logger.exception('Не удалось отправить Telegram-уведомление', key=key)


message_sender = MessageSender()
