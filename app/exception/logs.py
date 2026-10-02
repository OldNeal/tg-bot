from app.exception.base import BaseException

class LogsFilesException(BaseException):
    pass

class DontExistCategoryException(LogsFilesException):
    msg = 'Нет такой категории'

class DontHavePermissionException(LogsFilesException):
    msg = 'Нет доступа'

class DontLogFileException(LogsFilesException):
    msg = 'Только .log файлы'
