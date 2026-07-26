from app.aio.cls.msg.base import Templates, BaseText
from app.validate.api import AnswerBaseInfo

class MainText(BaseText):
    def __init__(self, data: AnswerBaseInfo):
        self.data: AnswerBaseInfo = data

    @property
    def info(self):
        member = [f'🏛 В организации не состоит']
        beyonder = [f'🔮 Обычный смертный']

        if self.data.member:
            member = [f'🏛 Организация: {self.data.member.organ_name}',
            f'⚜️ Ранг: {self.data.member.rank_name} ({self.data.member.rank})',
            f'🎖 Титул: {self.data.member.organ_name}']

        if self.data.beyonder:
            if self.data.beyonder.seq > 0:
                beyonder = [f'🔮 Путь: {self.data.beyonder.path_name}',
                f'🧪 Последовательноcть: {self.data.beyonder.seq} - {self.data.beyonder.seq_name}']
            elif self.data.beyonder.seq == 0:
                beyonder = [f'🎗 {self.data.beyonder.seq_name}']
            elif self.data.beyonder.seq < 0:
                beyonder = [f'🏵 {self.data.beyonder.seq_name}']

        return self.html(self.data.user.fullname).openmessage(self.data.user.tg_id) + self.html(self.html.joined([f'🏷 ID: {self.data.user.tg_id}'] + member + beyonder)).blockquote()

    @property
    def first_msg_by_info(self):
        return 'Держи карточку'

    def check_ping(api_ping: str | None = None):
        return f'⌛ Задержка API - {api_ping} мс.'