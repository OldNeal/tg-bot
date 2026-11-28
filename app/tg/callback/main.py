from app.tg.callback.base import BackCall, BaseCall, AccertCancelCall, PageCall

class MainCall(BaseCall, prefix='main'):
    pass

class MainInfoCall(MainCall, prefix='main_info'):
    purpose_tg_id: int

class MainBackCall(BackCall, prefix='main_back'):
    pass

class MyStateCall(MainCall, prefix='my_state'):
    pass

class MainUsersCall(MainCall, prefix='main_users'):
    pass

class MainUsersSearchCall(MainUsersCall, prefix='main_users_search'):
    pass

class MainUsersSearchFieldCall(MainUsersCall, prefix='main_users_search_field'):
    field: str

class MainUsersPageCall(PageCall, prefix='main_users_page'):
    pass

class MainUserInfoCall(MainCall, prefix='main_user_info'):
    user_id: int

class MainUserDeleteCall(MainCall, prefix='main_user_delete'):
    user_id: int
    confirmed: bool | None = None

class MainUserSettingsCall(MainCall, prefix='main_user_settings'):
    pass

class MainUserSettingsRedactCall(MainCall, prefix='main_user_settings_redact'):
    pass

class MainUserSettingsDefaultCall(MainCall, prefix='main_user_settings_default'):
    tag: str | None = None
    is_all: bool = False

class MainUserSettingsModeCall(MainCall, prefix='main_user_settings_mode'):
    is_json: bool = False

class MainUserSettingsGroupCall(MainCall, prefix='main_user_settings_group'):
    tag: str

class MainUserSettingsGroupDefaultCall(MainUserSettingsGroupCall, prefix='user_group_default'):
    pass

class MainUserSettingEditCall(MainCall, prefix='main_user_setting_edit'):
    tag: str
