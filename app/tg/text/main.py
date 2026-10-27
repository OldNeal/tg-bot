from app.tg.text.base import Templates, BaseText
from app.validate.api import AnswerBaseInfo

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
        user = self.data.purpose
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
        return self.user_mention(user) + self.html(self.html.joined([
            f'🏷 ID: {user_id} ({user.user_id})',
            f'🔗 Юз: {self.html(username or '❌').escape().openmessage(telegram.tg_id) if telegram else '❌'}'
            ] + member_text + beyonder_text)).blockquote()

    @property
    def first_msg_by_info(self):
        return 'Держи карточку'

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
        