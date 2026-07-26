from app.aio.cls.callback.base import BackCall, BaseCall

class WikiCall(BaseCall, prefix='wiki'):
    id: int

class WikiBackCall(BackCall, prefix='wiki_back'):
    pass

class SeqCall(WikiCall, prefix='wiki_seq'):
    pass

class PathCall(WikiCall, prefix='wiki_path'):
    pass

class GACall(WikiCall, prefix='wiki_ga'):
    pass

class GroupCall(BaseCall, prefix='wiki_group'):
    name: str
    type: str