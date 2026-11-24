from config import cmds
from app.tg.text.base import Templates, BaseText
from app.validate.core import AnswerBeyonderSistemInfo
from app.tg.text.emodzi import Emodzi


class HelpText(BaseText):
    @classmethod
    def cmds(self):
        return '📜 Все команды'+ self.html.separator(n=2) + self.html.joined([f'/{k} - {v}' for k, v in cmds.items()], sep=self.html.separator(n=2))

    @classmethod
    def main(self):
        return '📚 Меню справки'

    @classmethod
    def beyonder_sistem(self, data: AnswerBeyonderSistemInfo):
        return '⚗️ Система потусторонних' + self.html.separator(n=2) + self.html.joined([
            '🔼 В боте, чтобы перейти на следущюю последовательность нужно переваривать зелья опрделенное количество времени.',
            '⌛ Время можно ускорить, изучая метод действия',
            f'🧪 Таблица (посл. - дней - {Emodzi.activity_point_emodzi()} для 100% метода действия)'
        ], self.html.separator(n=2)) + self.html.joined([
            f'{seq.number} - {seq.days} дн. - {seq.rsp} {Emodzi.activity_point_emodzi()}' for seq in sorted(data.sequences, key=lambda x: x.number)
            ]).blockquote() + self.html.separator(n=2) + f'❗ Важно, тут указаны дни и {Emodzi.activity_point_emodzi()} для зелья 0 посл., но точное кол-во дней и {Emodzi.activity_point_emodzi()} зависит от кол-ва путей под ВД. Если путь один, то 30 дней, если путей 2, то 60 дней и т.д.'
    