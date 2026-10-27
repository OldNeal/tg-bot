from app.tg.text.base import Templates, BaseText
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
    def search(cls, value: str, count: int, page: int, max_page: int):
        if count == 0:
            return f'❌ По запросу «{cls.html(value).escape()}» ничего не найдено'
        return (
            f'🔎 По запросу «{cls.html(value).escape()}» найдено путей: {count} '
            f'[{page + 1}/{max_page} стр.]'
        )

    @classmethod
    def enter_search_value(self):
        return '✒️ Отправьте поисковой запрос'