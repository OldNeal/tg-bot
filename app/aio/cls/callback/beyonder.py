from app.aio.cls.callback.base import BackCall, BaseCall, AccertCancelCall, PageCall

class BeyonderCall(BaseCall, prefix='beyonder'):
    pass

class BeyonderInfoCall(BaseCall, prefix='beyonder_info'):
    purpose_tg_id: int

class BeyonderBackCall(BackCall, prefix='beyonder_back'):
    pass

class DrinkCall(BeyonderCall, prefix='drink'):
    path_id: int

class KillCall(AccertCancelCall, prefix='kill'):
    purpose_tg_id: int

class BeyonderListCall(AccertCancelCall, prefix='beyonder_list'):
    path_id: int

class BeyonderListPageCall(PageCall, prefix='beyonder_list_page'):
    path_id: int
    where: str | None = None