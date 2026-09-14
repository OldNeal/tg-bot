from app.aio.cls.callback.base import BackCall, BaseCall, AccertCancelCall

class MainCall(BaseCall, prefix='main'):
    pass

class MainBackCall(BackCall, prefix='main_back'):
    pass

class MyStateCall(MainCall, prefix='my_state'):
    pass