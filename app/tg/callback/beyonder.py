from app.tg.callback.base import BackCall, BaseCall, AccertCancelCall, PageCall

class BeyonderCall(BaseCall, prefix='beyonder'):
    pass

class BeyonderInfoCall(BaseCall, prefix='beyonder_info'):
    purpose_tg_id: int
    path_id: int | None = None
    page: int | None = None
    where: str | None = None

class BeyonderBackCall(BackCall, prefix='beyonder_back'):
    path_id: int | None = None
    page: int | None = None

class DrinkCall(BeyonderCall, prefix='drink'):
    path_id: int | None = None
    path_name: str | None = None
    purpose_tg_id: int | None = None
    seq: int | None = None

class BeyonderTimeInfoCall(BaseCall, prefix='beyonder_time_info'):
    purpose_tg_id: int

class BeyonderUpSeqCall(BaseCall, prefix='beyonder_upseq'):
    purpose_tg_id: int | None = None
    path_name: str | None = None
    path_id: int | None = None
    seq: int | None = None
    confirmed: bool | None = None

class KillCall(AccertCancelCall, prefix='kill'):
    purpose_tg_id: int

class BeyonderListCall(AccertCancelCall, prefix='beyonder_list'):
    path_id: int

class BeyonderListPageCall(PageCall, prefix='beyonder_list_page'):
    path_id: int
    where: str | None = None
    return_value: str | None = None
    return_page: int | None = None