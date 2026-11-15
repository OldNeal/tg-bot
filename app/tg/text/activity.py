from app.tg.text.base import BaseText
from app.validate.api import  (
    AnswerActivityPointsLimitReset,
    AnswerActivityPoints
)

class ActivityText(BaseText):
    @classmethod
    def activity(self, points: int):
        return f'🪙 Получены очки активности: {points}'

    def limit_reset(self, data: AnswerActivityPointsLimitReset):
        return f'🪙 У пользователя {self.user_mention(data.purpose)} был сброшен лимит получения очков активности'