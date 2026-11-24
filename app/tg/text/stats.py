from app.tg.text.base import Templates, BaseText
from app.validate.core import AnswerAllStats, AnswerBeyonderSistemInfo
from app.tg.text.emodzi import Emodzi

class StatsText(BaseText):

    @classmethod
    def all(self, data: AnswerAllStats):
        return '📊 Общая статистика' + self.html.joined([
            f'👥 Всего пользователей: {data.users}',
            f'{Emodzi.telegram_icon()} Телеграм-пользователей: {data.tg_users}',
            f'🧪 Всего потусторонних: {data.beyonders}',
            f'🎗️ Всего путей: {data.paths}',
            f'🏵 Всего ВД: {data.gas}',
            f'🎎 Всего участников: {data.members}',
            f'🏛️ Всего организаций: {data.organs}',
            f'❔ Всего вопросов: {data.questions}',
            f'📰 Всего газет: {data.news_papers}',
            f'{Emodzi.activity_point_emodzi()} Заработано: {data.activity_points_all_time}',
        ]).blockquote()
    
    @classmethod
    def search(cls, value: str, count: int, page: int, max_page: int):
        if count == 0:
            return f'❌ По запросу «{cls.html(value).escape()}» ничего не найдено'
        return f'🔎 По запросу «{cls.html(value).escape()}» найдено путей: {count} {cls.page_text(page, max_page)}'

    @classmethod
    def enter_search_value(self):
        return '✒️ Отправьте поисковой запрос'