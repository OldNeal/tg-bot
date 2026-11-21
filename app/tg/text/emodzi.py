from app.tg.text.base import BaseText

class Emodzi(BaseText):
    TELEGRAM_ICON_ID = 5346289081477248303

    @classmethod
    def telegram_icon(cls):
        return cls.html('📨').custom_emoji(cls.TELEGRAM_ICON_ID)

    @classmethod
    def activity_point_emodzi(self):
        return '💮'
