from app.validate.base import BaseValidate, Field
from datetime import datetime, timedelta

class BaseArg(BaseValidate):
    pass

class UserArg(BaseArg):
    purpose_tg_id: int | None = None

class UpDownSeqArg(UserArg):
    seq: int | None = None
    path_name: str | None = None

class DrinkArg(UserArg):
    seq: int = 9
    path_name: str

class TimeRedactArg(UserArg):
    duration: timedelta

class TimeReplaceArg(UserArg):
    datetime_arg: datetime



class NameArg(BaseArg):
    name: str

class SearchArg(BaseArg):
    value: str | None = None
    
class InfoOrganIdArg(UserArg):
    organ_id: int | None = None

class OrganIdArg(BaseArg):
    organ_id: int | None = None

class RankRedactArg(UserArg):   
    rank: int | None = None

class TitulRedactArg(UserArg):
    titul: str | None = None

class SettingRedactArg(UserArg):
    data: dict

