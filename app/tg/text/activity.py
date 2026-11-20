from app.tg.text.base import BaseText
from app.tg.text.emodzi import Emodzi
from app.validate.api import  (
    AnswerActivityPointsLimitReset,
    AnswerActivityPoints,
    AnswerActivityPointsLimit
)

class ActivityText(BaseText):
    @classmethod
    def activity(self, points: int):
        return f'{Emodzi.activity_point_emodzi()} Получены очки активности: {points}'

    @classmethod
    def limit_reset(self, data: AnswerActivityPointsLimitReset):
        return f'⚡ У пользователя {self.user_mention(data.purpose)} был сброшен лимит получения очков активности'
    
    @classmethod
    def limits(self, data: AnswerActivityPointsLimit):
        ap_emodzi = Emodzi.activity_point_emodzi()
        return f'⚡ Лимиты активности' + self.html.separator().join([
            (f'➕ Получено недавно: {data.used} / {data.limit} {ap_emodzi}' if data.remaining > 0 else '😢 Вы исчерпали лимит награды за активность'),
            f'🎖️ Награда за сообщение: {data.points_per_message} {ap_emodzi}',
            f'⛅ Лимиты сбрасываются каждый день',
        ]).blockquote()