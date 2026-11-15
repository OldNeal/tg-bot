from app.exception.base import BotError


class ActivityMessageTooShortError(BotError):
    msg = 'Сообщение слишком короткое для начисления активности'

class ActivityLowDiversityError(BotError):
    msg = 'В сообщении недостаточно разнообразного текста'

class ActivityCooldownError(BotError):
    msg = 'Активность можно засчитывать не чаще одного раза в минуту'

class ActivityDuplicateError(BotError):
    msg = 'Похожее сообщение уже учитывалось'

class ActivityMessagePerRequestError(BotError):
    msg = 'Сообщения отправляются вместе'
