from app.tg.callback.base import BaseCall, PageCall


class QuestionMenuCall(BaseCall, prefix='question_menu'):
    action: str
    page: int = 0


class QuestionCreateCall(BaseCall, prefix='question_create'):
    action: str
    field: str = ''
    is_anonim: bool = False


class QuestionSelectCall(BaseCall, prefix='question_select'):
    page: int
    index: int


class QuestionQuizAnswerCall(BaseCall, prefix='question_quiz_answer'):
    question_id: int
    answer_id: int


class QuestionModerationCall(BaseCall, prefix='question_moderation'):
    action: str
    field: str = ''
    is_check: bool = False


class QuestionPageCall(PageCall, prefix='question_page'):
    pass
