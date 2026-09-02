from app.aio.cls.msg.base import Templates, BaseText
from app.validate.api import AnswerAllStats

class StatsText(BaseText):

    @classmethod
    def all(self, data: AnswerAllStats):
        return '📊 Общая статистика' + self.html.joined([
            f'👥 Всего пользователей: {data.users}',
            f'🧪 Всего потусторонних: {data.beyonders}',
            f'🎗️ Всего путей: {data.paths}',
            f'🏵 Всего ВД: {data.gas}',
            f'🎎 Всего участников: {data.members}',
            f'🏛️ Всего организаций: {data.organs}',
        ]).blockquote()