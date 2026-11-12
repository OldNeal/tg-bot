from app.tg.text.base import BaseText
from app.validate.api import  (
    AnswerActivityPointsLimitReset,
    AnswerActivityPoints,
    AnswerActivityPointsAdd,
    AnswerActivityPointsDeduct,
)

class ActivityText(BaseText):
    @classmethod
    def activity(self, points: int):
        return f'🪙 Получены очки активности: {points}'

    @classmethod
    def added(self, data: AnswerActivityPointsAdd):
        return self.user_mention(data.purpose) + self.html.separator().join([
            f'⌛ Было: {data.old_activity_points}',
            f'🪙 Стало: {data.activity_points}',
            f'➕ Добавлено: {data.added_activity_points}',
        ])

    @classmethod
    def deducted(self, data: AnswerActivityPointsDeduct):
        return self.user_mention(data.purpose) + self.html.separator().join([
            f'⌛ Было: {data.old_activity_points}',
            f'🪙 Стало: {data.activity_points}',
            f'➖ Удалено: {data.deducted_activity_points}',
        ])
    
    @classmethod
    def reset(self, data: AnswerActivityPoints):
        return self.user_mention(data.purpose) + self.html.separator().join([
            f'⌛ Было: {data.activity_points}',
            f'🪙 Стало: 0',
        ])

    @classmethod
    def limit_reset(self, data: AnswerActivityPointsLimitReset):
        return f'🪙 У пользователя {self.user_mention(data.purpose)} был сброшен лимит получения очков активности'