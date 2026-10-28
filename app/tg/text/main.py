from app.tg.text.base import Templates, BaseText
from app.validate.api import AnswerBaseInfo, AnswerUserBody

class MainText(BaseText):
    def __init__(self, data: AnswerBaseInfo):
        self.data: AnswerBaseInfo = data

    @classmethod
    def menu(self):
        return '🧭 Главное меню'

    @property
    def info(self):
        member_text = [f'🏛 В организации не состоит']
        beyonder_text = [f'🔮 Обычный смертный']

        member = self.data.member
        beyonder = self.data.beyonder
        user = self.data.purpose or self.data.user
        telegram = user.telegram

        if member:
            member_text = [f'🏛 Организация: {member.organ_name}',
            f'⚜️ Ранг: {member.rank_name} ({member.rank})']
            if member.titul:
                member_text.append(f'🎖 Титул: {self.html(member.titul).escape()}')

        if beyonder:
            if beyonder.seq > 0:
                beyonder_text = [f'🔮 Путь: {beyonder.path_name}',
                f'🧪 Последовательноcть: {beyonder.seq} - {beyonder.seq_name}']
            elif beyonder.seq == 0:
                beyonder_text = [f'🎗 {beyonder.seq_name}']
            elif beyonder.seq < 0:
                beyonder_text = [f'🏵 {beyonder.seq_name}']

        user_id = telegram.tg_id if telegram else user.user_id
        username = telegram.username if telegram else None
        return '🪪 ' + self.user_mention(user) + self.html(self.html.joined([
            f'🏷 ID: {user_id} ({user.user_id})',
            f'🔗 Юз: {self.html(username or '❌').escape().openmessage(telegram.tg_id) if telegram else '❌'}'
            ] + member_text + beyonder_text)).blockquote()

    @classmethod
    def check_ping(self, api_ping: str | None = None):
        return f'⌛ Задержка API - {api_ping} мс.'

    @classmethod
    def state_clear(self):
        return f'✅ Куки очищены'

    @classmethod
    def state_pop(self):
        return f'✅ Кук удален'

    @classmethod
    def state_dont_pop(self):
        return f'❌ Кук не найден'

    @classmethod
    def users_list(cls, count: int, page: int, max_page: int):
        if not count:
            return '❌ Пользователей нет'
        return f'👥 Пользователи: {count} [{page + 1}/{max_page} стр.]'

    @classmethod
    def users_search_fields(cls):
        return '🔎 Выберите критерий поиска'

    @classmethod
    def users_search_input(cls, field: str):
        labels = {
            'user_id': 'внутренний ID',
            'tg_id': 'Telegram ID',
            'username': 'username',
            'name': 'имя',
        }
        return f'✒️ Введите {labels[field]} пользователя'

    @classmethod
    def users_search_results(cls, count: int, page: int, max_page: int):
        if not count:
            return '❌ Пользователи по этому запросу не найдены'
        return f'🔎 Найдено пользователей: {count} [{page + 1}/{max_page} стр.]'

    @classmethod
    def user_info(cls, user: AnswerUserBody):
        telegram = user.telegram
        details = [
            f'🏷 Внутренний ID: {user.user_id}',
            f'🪦 Имя: {cls.html(user.name or "❌").escape().openmessage(user.telegram.tg_id)}',
            f'🆔 Telegram ID: {telegram.tg_id if telegram else "❌"}',
            f'🔗 Username: {cls.user_mention(user)}',
        ]
        return '👤 Аккаунт' + cls.html(cls.html.joined(details)).blockquote()

    @classmethod
    def user_deleted(cls, user: AnswerUserBody):
        return f'✅ {cls.html('Ваш').escape().openmessage(user.telegram.tg_id)} аккаунт удалён. Если вы продолжите использовать бота, то он создаст вам новый аккаунт.'

    @classmethod
    def user_delete_cancelled(cls):
        return '🗑 Удаление аккаунта отменено'

    @classmethod
    def user_delete_confirm(cls, user: AnswerUserBody):
        return f'🗑 {cls.html('Вы').escape().openmessage(user.telegram.tg_id)} хотите удалить свой аккаунт?'
