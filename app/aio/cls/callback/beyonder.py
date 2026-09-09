from app.aio.cls.callback.base import BackCall, BaseCall, AccertCancelCall

class BeyonderCall(BaseCall, prefix='beyonder'):
    pass

class BeyonderBackCall(BackCall, prefix='beyonder_back'):
    pass

class DrinkCall(BaseCall, prefix='drink'):
    path_id: int

class KillCall(AccertCancelCall, prefix='kill'):
    purpose_tg_id: int