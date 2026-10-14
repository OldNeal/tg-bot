from datetime import datetime, timedelta
from app.validate.base import BaseValidate

class BaseTextValidate(BaseValidate):
    pass

class UserTextValidate(BaseTextValidate):
    name: str

class RedactSeqTextValidate(UserTextValidate):
    seq_name: str
    path_name: str