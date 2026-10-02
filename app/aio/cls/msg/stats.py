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
    
    @classmethod
    def search(cls, max_page: int, page: int, value: str, results: int = 0):
        return f'🔎 По запросу "{value}" найдены пути ({results} шт.) {f'[{page+1}/{max_page} стр.]' if max_page > 1 else ''}' if results > 0 else '❌ Ничего не найдено'
    
    