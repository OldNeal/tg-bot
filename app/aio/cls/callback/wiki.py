from app.aio.cls.callback.base import BackCall, BaseCall, PageCall

class WikiCall(BaseCall, prefix='wiki'):
    id: int

class WikiBackCall(BackCall, prefix='wiki_back'):
    is_all: bool | None = None

class SeqCall(WikiCall, prefix='wiki_seq'):
    pass

class PathCall(WikiCall, prefix='wiki_path'):
    pass

class GACall(WikiCall, prefix='wiki_ga'):
    pass

class GroupCall(BaseCall, prefix='wiki_group'):
    name: str
    type: str

class WikiSearchCall(BaseCall, prefix='wiki_search'):
    type: str

class WikiMenuCall(BaseCall, prefix='wiki_menu'):
    type: str

class PathsPageCall(PageCall, prefix='wiki_paths_page'):
    value: str

class GasPageCall(PathsPageCall, prefix='wiki_gas_page'):
    pass