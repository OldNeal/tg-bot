from app.exception.base import BotError


class BeyonderMethodActionPointsError(BotError):
    msg = 'Введите положительное целое число очков'

class BeyonderMethodActionStateError(BotError):
    msg = 'Не удалось найти запрос на изучение метода действия. Запустите действие заново.'

class BeyonderUpseqError(BotError):
    msg = 'Продвинуться может только сам потусторонний.'