from app.aio.cls.callback.base import BackCall, BaseCall, PageCall

class StatsCall(BaseCall, prefix='stats'):
    pass

class StatsBackCall(BackCall, prefix='stats_back'):
    pass

class StatsPathsCall(StatsCall, prefix='stats_paths'):
    pass

class StatsPageCall(PageCall, prefix='stats_page'):
    page: int
    value: str