from app.validate.base import BaseValidate
from datetime import datetime, timedelta

class BaseArg(BaseValidate):
    pass

class UserArg(BaseArg):
    purpose_tg_id: int | None = None

class UpDownSeqArg(UserArg):
    seq: int = 1
    path_name: str | None = None

class DrinkArg(UserArg):
    seq: int = 9
    path_name: str

class TimeRedactArg(UserArg):
    duration: timedelta

class TimeReplaceArg(UserArg):
    date: datetime



class NameArg(BaseArg):
    name: str

class SearchArg(BaseArg):
    value: str

