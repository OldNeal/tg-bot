from app.tg.callback.base import BaseCall, PageCall


class QuestionMenuCall(BaseCall, prefix='question_menu'):
    action: str = 'menu'
    page: int = 0


class QuestionMineCall(BaseCall, prefix='question_mine'):
    page: int = 0


class QuestionRandomCall(BaseCall, prefix='question_random'):
    pass


class QuestionRandomDifficultyCall(BaseCall, prefix='question_random_difficulty'):
    difficulty: int


class QuestionStartCreateCall(BaseCall, prefix='question_start_create'):
    pass


class QuestionStartJsonCreateCall(BaseCall, prefix='question_start_json'):
    pass

class QuestionEditCall(BaseCall, prefix='question_edit'):
    action: str = 'open'
    question_id: int = 0
    field: str = ''


class QuestionUserStatsCall(BaseCall, prefix='question_userstats'):
    pass


class QuestionLimitsCall(BaseCall, prefix='question_limits'):
    pass


class QuestionLeaveQuizCall(BaseCall, prefix='question_leave_quiz'):
    pass


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


class PendingQuestionsRefreshCall(BaseCall, prefix='pending_questions_refresh'):
    is_check: bool = False


class QuestionPageCall(PageCall, prefix='question_page'):
    pass
