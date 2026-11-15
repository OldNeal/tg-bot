from app.exception.base import BotError


class ItemUnknownActionError(BotError):
    msg = 'Неизвестная подкоманда, доступные подкоманды: give, take'


class ItemCommandValueError(BotError):
    msg = 'ID предмета и количество должны быть положительными числами'


class ItemCommandStateError(BotError):
    msg = 'Не удалось восстановить меню изменения предмета, откройте карточку заново'
