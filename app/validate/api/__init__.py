from app.api.schemas import *
from app.api.schemas import AnswerPathFullInfo as AnswerPathFullInfoApi

class AnswerPathFullInfo(AnswerPathFullInfoApi):
    @property
    def seq_dict(self):
        return {s.number:s for s in self.seqs}

    @property
    def god(self):
        return self.seq_dict.get(0)
