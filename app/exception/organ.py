from app.exception.base import BotError

class ALreadyMemberError(BotError):
    msg = 'Пользователь уже участник организации'