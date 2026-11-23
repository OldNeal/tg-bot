from app.core.schemas import *
from app.core.schemas import AnswerPathFullInfo as AnswerPathFullInfoCore

class AnswerPathFullInfo(AnswerPathFullInfoCore):
    @property
    def seq_dict(self):
        return {s.number:s for s in self.seqs}

    @property
    def god(self):
        return self.seq_dict.get(0)
