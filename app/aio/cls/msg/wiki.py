from app.aio.cls.msg.base import Templates, BaseText
from app.validate.api import AnswerAllPathInfo

class PathText(BaseText):
    def __init__(self, data: AnswerAllPathInfo):
        super().__init__(data)
        self.data: AnswerAllPathInfo = self.data

    @property
    def all(self):
        return '📜 Все пути'
    
class WikiText:
    path = PathText