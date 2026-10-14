from config import cmds
from app.aio.cls.msg.base import Templates, BaseText

class HelpText(BaseText):
    @classmethod
    def main(self):
        return '📜 Все команды'+ self.html.br(2) + self.html.joined([f'/{k} - {v}' for k, v in cmds.items()], sep=self.html.br(2))