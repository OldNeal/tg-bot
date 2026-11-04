from app.exception.base import BotError

class AnswerCorrectError(BotError):
    msg = 'Добавьте хотя бы один правильный ответ, каждый с новой строки'

class AnswerInCorrectError(BotError):
    msg = 'Добавьте хотя бы 3 неправильных ответа, каждый с новой строки'  

class QuestionBodyError(BotError):
    msg = 'Текст вопроса не может быть пустым'  
    
class QuestionAnswersError(BotError):
    msg = 'Для вопроса нужны минимум 1 правильный и 3 неправильных ответа'  

class QuestionExpiredError(BotError):
    msg = 'Этот вопрос уже недоступен. Запросите случайный вопрос заново'  

class QuestionPrivateChatError(BotError):
    msg = 'Эта функция доступна только в личном чате с ботом'

class QuestionModerationPermissionError(BotError):
    msg = 'Модерировать заявки могут только администраторы группы модерации'

class QuestionModerationRequestError(BotError):
    msg = 'Заявка на модерацию недействительна или уже обработана'

class QuestionModerationPendingError(BotError):
    msg = 'У вас уже есть вопрос, ожидающий модерации'

class QuestionModerationReasonError(BotError):
    msg = 'Укажите причину отказа'