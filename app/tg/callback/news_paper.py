from typing import Literal

from app.tg.callback.base import AccertCancelCall, BaseCall

class NewsPaperCall(BaseCall, prefix='news_paper'):
    pass

class NewsPaperSearchCall(NewsPaperCall, prefix='news_paper_search'):
    pass

class NewsPaperCreateCall(NewsPaperCall, prefix='news_paper_create'):
    pass

class NewsPaperMenuCall(NewsPaperCall, prefix='news_paper_menu'):
    pass

class NewsPaperPageCall(NewsPaperCall, prefix='news_paper_page'):
    page: int
    mode: Literal[
        'search', 'all', 'list', 'editors', 'readers',
        'subscribe', 'unsubscribe', 'notify', 'make_editor', 'fire_editor',
    ] = 'search'
    news_paper_id: int | None = None

class NewsPaperActionCall(NewsPaperCall, prefix='news_paper_action'):
    action: Literal['subscribe', 'unsubscribe', 'notify', 'make_editor', 'fire_editor']
    news_paper_id: int

class ReaderCall(NewsPaperCall, prefix='reader'):
    purpose_tg_id: int
    news_paper_id: int

class NewsPaperSubscribeCall(NewsPaperCall, prefix='news_paper_subscribe'):
    news_paper_id: int

class NewsPaperUnsubscribeCall(NewsPaperCall, AccertCancelCall, prefix='news_paper_unsubscribe'):
    news_paper_id: int

class NewsPaperNotifyCall(NewsPaperCall, prefix='news_paper_notify'):
    news_paper_id: int

class NewsPaperCaptureCall(NewsPaperCall, prefix='news_paper_capture'):
    news_paper_id: int

class NewsPaperMakeEditorCall(ReaderCall, prefix='news_paper_make_editor'):
    pass

class NewsPaperFireEditorCall(ReaderCall, prefix='news_paper_fire_editor'):
    pass

class NewsPaperGiveCall(ReaderCall, AccertCancelCall, prefix='news_paper_give'):
    pass

class NewsPaperInfoCall(NewsPaperCall, prefix='news_paper_info'):
    news_paper_id: int

class NewsPaperInfoDescCall(NewsPaperInfoCall, prefix='news_paper_info_desc'):
    pass

class NewsPaperSettingsCall(NewsPaperCall, prefix='news_paper_settings'):
    news_paper_id: int

class NewsPaperSettingsRedactCall(NewsPaperSettingsCall, prefix='news_paper_settings_redact'):
    pass

class NewsPaperSettingsDefaultCall(NewsPaperSettingsCall, prefix='news_paper_settings_default'):
    pass
