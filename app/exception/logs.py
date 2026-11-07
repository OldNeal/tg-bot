from app.exception.base import BotError

class LogsFilesException(BotError):
    pass

class DontExistCategoryException(LogsFilesException):
    msg = 'Нет такой категории'

class DontHavePermissionException(LogsFilesException):
    msg = 'Нет доступа'

class DontLogFileException(LogsFilesException):
    msg = 'Только .log файлы'
