from config import cmds
from app.tg.text.base import Templates, BaseText

class HelpText(BaseText):
    @classmethod
    def main(self):
        return '📜 Все команды'+ self.html.separator(n=2) + self.html.joined([f'/{k} - {v}' for k, v in cmds.items()], sep=self.html.separator(n=2))