from app.tg.text.base import BaseText
from app.api.schemas import AnswerNewsPaperGive, AnswerNewsPaperInfoDescription, AnswerNewsPaperInfoReaders, AnswerReaderInfo, NewsPaperInfo

class NewsPaperText(BaseText):
    @classmethod
    def search(cls, value: str, count: int, page: int, max_page: int):
        if count == 0:
            return f'❌ По запросу «{cls.html(value).escape()}» ничего не найдено'
        return (
            f'🔎 По запросу «{cls.html(value).escape()}» найдено газет: {count} '
            f'[{page + 1}/{max_page} стр.]'
        )

    @classmethod
    def my_list(cls, count: int, page: int, max_page: int):
        if count == 0:
            return '❌ Вы не подписаны ни на одну газету'
        return f'📰 Газеты, на которые вы подписаны: {count} [{page + 1}/{max_page} стр.]'

    @classmethod
    def all(cls, count: int, page: int, max_page: int):
        if count == 0:
            return '❌ Газет нет'
        return f'📰 Все газеты: {count} [{page + 1}/{max_page} стр.]'
    
    @classmethod
    def choose_news_paper(cls, action: str, count: int, page: int, max_page: int):
        if count == 0:
            return '❌ Газет нет'
        action_names = {
            'subscribe': 'подписки',
            'unsubscribe': 'отписки',
            'notify': 'уведомления',
            'make_editor': 'назначения редактора',
            'fire_editor': 'снятия редактора',
        }
        return f'📰 Выберите газету для {action_names[action]} [{page + 1}/{max_page} стр.]'

    @classmethod
    def editors(cls, count: int, page: int, max_page: int):
        if count == 0:
            return '❌ Вы не редактор ни одной газеты'
        return f'✒️ Газеты, где вы редактор: {count} [{page + 1}/{max_page} стр.]'

    @classmethod
    def readers(
        cls,
        news_paper_name: str,
        page: int,
        max_page: int,
    ):
        if max_page == 0:
            return f'❌ У газеты «{cls.html(news_paper_name).escape()}» нет читателей'

        return f'👥 Читатели газеты «{cls.html(news_paper_name).escape()}» [{page + 1}/{max_page} стр.]'

    @classmethod
    def created(cls, news_paper: NewsPaperInfo):
        return f'➕ Создана газета «{cls.html(news_paper.name).escape()}»'

    @classmethod
    def to_search(cls):
        return '✒️ Введите название газеты для поиска'

    @classmethod
    def to_create(cls):
        return '✒️ Отправьте название новой газеты'

    @classmethod
    def info(cls, news_paper: NewsPaperInfo):
        return f'{cls.html(news_paper.emodzi or "📰").emoji(news_paper.custom_emodzi_id)} {cls.html(news_paper.name).escape()}' + cls.html.joined([
            f'🏷 ID: {news_paper.id}',
            f'👥 Читателей: {news_paper.reader_counts}',
        ]).blockquote()

    @classmethod
    def description(cls, data: AnswerNewsPaperInfoDescription):
        if not data.description:
            return '🪶 Описание отсутствует'
        return cls.html('🪶 Описание').separator(n=2) + cls.html(data.description).escape()

    @classmethod
    def capture(cls, news_paper: NewsPaperInfo):
        return f'👑 Вы захватили газету «{cls.html(news_paper.name).escape()}»'

    @classmethod
    def settings_values(cls, values: dict):
        return '⚙️ Настройки' + cls.html.json_format(values, indent=4).escape().code().pre('json')

    @classmethod
    def to_enter_settings(cls):
        return '✒️ Отправьте новые настройки в формате JSON'
    
    @classmethod
    def reader(self, user: AnswerReaderInfo):
        if user.reader:
            reader = [
            f'📰 Газета: {user.reader.news_paper_name}',
            f'👤 Кто: {user.reader.rank_name}'
            ]
        telegram = user.purpose.telegram
        user_id = telegram.tg_id if telegram else user.purpose.user_id
        username = telegram.username if telegram else None
        return '🗞 ' + self.user_mention(user.purpose) + self.html(self.html.joined([
            f'🏷 ID: {user_id} ({user.purpose.user_id})',
            f'🔗 Юз: {self.html(username or '❌').escape().openmessage(telegram.tg_id) if telegram else '❌'}'
            ] + reader)).blockquote()

    @classmethod
    def menu(self):
        return '📰 Меню'

    @classmethod
    def sub(self, tg_id: int, news_paper_name: str):
        return f'🔔 {self.html('Вы').openmessage(tg_id)} подписались на газету {news_paper_name}'

    @classmethod
    def unsub(self, tg_id: int, news_paper_name: str):
        return f'🔕 {self.html('Вы').openmessage(tg_id)} отписались от газеты {news_paper_name}'

    @classmethod
    def confirm_unsub(cls, news_paper: NewsPaperInfo):
        return f'❔ Отписаться от газеты «{cls.html(news_paper.name).escape()}»?'

    @classmethod
    def make(self, tg_id: int, purpose_tg_id: int, purpose_name: str, news_paper_name: str):
        return f'🔼 {self.html('Вы').openmessage(tg_id)} сделали {self.html(purpose_name).openmessage(purpose_tg_id)} редактором газеты {news_paper_name}'

    @classmethod
    def fire(self, tg_id: int, purpose_tg_id: int, purpose_name: str, news_paper_name: str):
        return f'🔽  {self.html('Вы').openmessage(tg_id)} сняли {self.html(purpose_name).openmessage(purpose_tg_id)} с поста редактора газеты {news_paper_name}'

    @classmethod
    def to_give(cls, reader: AnswerReaderInfo):
        return f'👑 Передать газету пользователю {cls.user_mention(reader.user)}?'

    @classmethod
    def give(cls, data: AnswerNewsPaperGive):
        if data.purpose is None:
            raise ValueError('API response is missing the recipient')
        return f'👑 Газета передана пользователю {cls.user_mention(data.purpose)}'

    @classmethod
    def notify(self, datas: dict[int, str]):
        return self.html.joined([self.html(text).openmessage(tg_id) for tg_id, text in datas.items()], ' ')    
    
    @classmethod
    def to_notify(self, news_paper_id: int):
        return '🔔 Ответьте на нужное сообщение командой - ' + self.html(f'/notify {news_paper_id}').code()