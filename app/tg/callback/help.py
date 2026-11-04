from app.tg.callback.base import BackCall, BaseCall, AccertCancelCall, PageCall

class HelpCall(BaseCall, prefix='help'):
    pass

class CmdListCall(BaseCall, prefix='cmd_list'):
    pass