from app.aio.cls.msg.base import Templates, BaseText
from app.validate.api import AnswerAllPathInfo, AnswerPathFullInfo, AnswerGAFullInfo, AnswerGASearchInfo

class PathText(BaseText):
    def __init__(self, data: AnswerAllPathInfo | AnswerPathFullInfo):
        self.data = data

    @property
    def all(self):
        return '📜 Все пути'

    def info(self, value: str | None = None):
        return self.html(f'🏵 {self.data.ga.name}') + self.html.joined([f'{s.number} - {s.name}' for s in sorted(self.data.seqs, key=lambda x: x.number)]).blockquote()

    @classmethod
    def search(cls, value: str, results: int = 0):
        return f'''🔎 По запросу "{value}" найдены пути ({results} шт.)''' if results > 0 else '❌ Ничего не найдено'
    
class GAText(BaseText):
    def __init__(self, data: AnswerGASearchInfo | AnswerGAFullInfo):
        self.data = data

    @property
    def all(self):
        return '📜 Все Великие Древние'

    def info(self, value: str | None = None):
        return self.html(f'🏵 {self.data.name}') 

    @classmethod
    def search(cls, value: str, results: int = 0):
        return f'''🔎 По запросу "{value}" найдены Великие Древние ({results} шт.)''' if results > 0 else '❌ Ничего не найдено'
    
class WikiText:
    path = PathText
    ga = GAText