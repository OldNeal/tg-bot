from app.aio.cls.callback.base import BackCall, BaseCall, PageCall, AccertCancelCall

class OrganCall(BaseCall, prefix='organ'):
    pass

class OrganBackCall(BackCall, prefix='organ_back'):
    pass

class OrganPageCall(PageCall, prefix='organ_page'):
    is_search: bool

class OrganInfoCall(OrganCall, prefix='organ_info'):
    organ_id: int | None = None
    purpose_tg_id: int | None = None

class OrganMemberPageCall(PageCall, OrganInfoCall, prefix='organ_member_page'):
    pass

class OrganInfoDescCall(OrganInfoCall, prefix='organ_info_desc'):
    pass

class OrganInfoMembersCall(OrganInfoCall, prefix='organ_info_members'):
    pass





class OrganSettingParametrCall(OrganCall, prefix='organ_setting_parametr'):
    tag: str
    value: str | int | bool
    type: str

class OrganSettingGroupCall(OrganCall, prefix='organ_setting_group'):
    tag: str

class OrganSettingModeCall(OrganCall, prefix='organ_setting_mode'):
    is_json: bool = False

class OrganSettingParametrDefaultCall(OrganCall, prefix='organ_setting_parametr_default'):
    tag: str | None = None
    is_all: bool = False

class OrganSettingParametrBooleanCall(OrganCall, prefix='organ_setting_parametr_boolean'):
    tag: str

class OrganSettingRedactCall(OrganCall, prefix='organ_setting_redact'):
    pass

class OrganSettingCall(OrganCall, prefix='organ_setting'):
    pass



class OrganMemberCall(OrganCall, prefix='organ_member'):
    purpose_tg_id: int

class OrganRankRedactCall(OrganMemberCall, prefix='organ_rank_redact'):
    operation: str

class OrganTitulRedactCall(OrganMemberCall, prefix='organ_titul_redact'):
    pass

class OrganTitulDeleteCall(OrganMemberCall, prefix='organ_titul_delete'):
    pass

class OrganLoginCall(OrganInfoCall, prefix='organ_login'):
    pass

class OrganCaptureCall(OrganCall, prefix='organ_capture'):
    pass

class OrganSearchCall(OrganCall, prefix='organ_search'):
    pass

class OrganExitCall(OrganCall, AccertCancelCall, prefix='organ_exit'):
    pass

class OrganKickCall(OrganMemberCall, AccertCancelCall, prefix='organ_kick'):
    pass

class OrganGiveCall(OrganMemberCall, AccertCancelCall, prefix='organ_give'):
    pass
