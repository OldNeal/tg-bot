from __future__ import annotations

import inspect
import typing
import decimal
import enum

import pydantic

from clientele.schemas import ListResponse  # noqa

class AnswerAllGAInfo(pydantic.BaseModel):
    gas: list["AnswerGAInfo"] | None


class AnswerAllGroupInfo(pydantic.BaseModel):
    groups: list[str]


class AnswerAllNewsPaperInfo(pydantic.BaseModel):
    search_value: typing.Optional[str | None] = None
    news_papers: list["NewsPaperInfo"]


class AnswerAllOrganInfo(pydantic.BaseModel):
    search_value: typing.Optional[str | None] = None
    organs: list["OrganInfo"]


class AnswerAllPathInfo(pydantic.BaseModel):
    paths: list["AnswerPathInfo"] | None


class AnswerAllSeqInfo(pydantic.BaseModel):
    seqs: list["AnswerSeqInfo"] | None


class AnswerAllStats(pydantic.BaseModel):
    users: int
    beyonders: int
    members: int
    organs: int
    paths: int
    gas: int


class AnswerBaseInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    beyonder: typing.Optional[typing.Union["BeyonderInfo", None]] = None
    member: typing.Optional[typing.Union["MemberInfo", None]] = None


class AnswerBeyonderInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    beyonder: typing.Optional[typing.Union["BeyonderInfo", None]] = None
    for_buttons: typing.Optional[typing.Union["ForButtons", None]] = None


class AnswerBeyonderList(pydantic.BaseModel):
    path: "AnswerPathInfo"
    ga: typing.Optional[typing.Union["AnswerBeyonderInfo", None]] = None
    beyonders: list["AnswerBeyonderInfo"]


class AnswerBody(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None


class AnswerGAFullInfo(pydantic.BaseModel):
    group: str
    name: str
    ga_id: int
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None
    paths: list["AnswerPathInfo"]


class AnswerGAInfo(pydantic.BaseModel):
    group: str
    name: str
    ga_id: int
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None


class AnswerGASearchInfo(pydantic.BaseModel):
    search_value: str | None
    gas: list["AnswerGAInfo"] | None


class AnswerGroupInfo(pydantic.BaseModel):
    group_name: str
    gas: list["AnswerGAInfo"]


class AnswerLogFileNames(pydantic.BaseModel):
    names: list[str]


class AnswerMain(pydantic.BaseModel):
    message: str
    version: str


class AnswerMemberInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    member: typing.Optional[typing.Union["MemberInfo", None]] = None
    for_buttons: typing.Optional[typing.Union["ForButtons", None]] = None


class AnswerNewsPaperGive(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None


class AnswerNewsPaperInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    news_paper: "NewsPaperInfo"
    for_buttons: typing.Optional[typing.Union["ForButtons", None]] = None


class AnswerNewsPaperInfoDescription(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    id: int
    name: str
    description: typing.Optional[str | None] = None


class AnswerNewsPaperInfoReaders(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    id: int
    name: str
    readers: list["AnswerReaderInfo"]


class AnswerNewsPaperSetting(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    settings: "OrganSettingValidate"


class AnswerNewsPaperSettingValues(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    values: dict[str, typing.Any]


class AnswerOrganGive(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None


class AnswerOrganInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    organ: "OrganInfo"
    for_buttons: typing.Optional[typing.Union["ForButtons", None]] = None


class AnswerOrganInfoDescription(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    id: int
    name: str
    description: typing.Optional[str | None] = None


class AnswerOrganInfoMembers(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    id: int
    name: str
    members: list["AnswerMemberInfo"]


class AnswerOrganSetting(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    settings: "OrganSettingValidate"


class AnswerOrganSettingValues(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    values: dict[str, typing.Any]


class AnswerPathFullInfo(pydantic.BaseModel):
    group: str
    name: str
    path_id: int
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None
    ga: "AnswerGAInfo"
    seqs: list["AnswerSeqInfo"]


class AnswerPathInfo(pydantic.BaseModel):
    group: str
    name: str
    path_id: int
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None


class AnswerPathSearchInfo(pydantic.BaseModel):
    search_value: str | None
    paths: list["AnswerPathInfo"] | None


class AnswerReaderInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    reader: typing.Optional[typing.Union["ReaderInfo", None]] = None
    for_buttons: typing.Optional[typing.Union["ForButtons", None]] = None


class AnswerRedactSeq(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    old: typing.Optional[typing.Union["Sequence", None]] = None
    new: typing.Optional[typing.Union["Sequence", None]] = None
    operation: str


class AnswerRedactTitul(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    new_titul: typing.Optional[str | None] = None
    old_titul: typing.Optional[str | None] = None


class AnswerSeqFullInfo(pydantic.BaseModel):
    number: int
    name: str
    path_id: int
    seq_id: int
    path_name: typing.Optional[str | None] = None


class AnswerSeqInfo(pydantic.BaseModel):
    number: int
    name: str
    path_id: int
    seq_id: int


class AnswerSeqSearchInfo(pydantic.BaseModel):
    search_value: str | None
    seqs: list["AnswerSeqInfo"] | None


class AnswerTimeInfo(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    next_upseq: str | None
    last_upseq: str
    upseq_days: int | None


class AnswerTimeRedact(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    old_time: str
    new_time: str
    seconds: int
    operator: str


class AnswerTimeReplace(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    old_time: str
    new_time: str


class AnswerUserBody(pydantic.BaseModel):
    user_id: int
    name: typing.Optional[str | None] = None
    telegram: typing.Optional[typing.Union["TelegramBody", None]] = None


class BaseExceptionResponse(pydantic.BaseModel):
    message: str
    status_code: int
    headers: typing.Optional[dict[str, typing.Any] | None] = None
    content: typing.Optional[typing.Any] = None


class BeyonderInfo(pydantic.BaseModel):
    path_name: str | None
    seq: int | None
    seq_name: str | None
    emodzi: str | None
    custom_emodzi_id: str | None


class ForButtons(pydantic.BaseModel):
    is_member: bool = False
    is_reader: bool = False
    organ_id: int | None
    news_paper_id: int | None
    is_redact_setting: bool = False
    is_redact_rank: bool = False
    is_redact_titul: bool = False
    is_kick: bool = False
    is_capture: bool = False
    is_give: bool = False
    is_news: bool = False


class HTTPValidationError(pydantic.BaseModel):
    detail: list["ValidationError"]


class MemberInfo(pydantic.BaseModel):
    titul: str | None
    organ_name: str | None
    organ_id: int | None
    rank: int | None
    rank_name: str | None
    login_at: str | None


class NewsPaperInfo(pydantic.BaseModel):
    id: int
    name: str
    owner: typing.Optional[typing.Union["AnswerReaderInfo", None]] = None
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None
    reader_counts: int = 0


class OrganInfo(pydantic.BaseModel):
    id: int
    name: str
    owner: typing.Optional[typing.Union["AnswerMemberInfo", None]] = None
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None
    member_counts: int = 0
    created_at: str


class OrganSettingDefault(pydantic.BaseModel):
    parametr: str | None
    group: str | None
    is_all: bool = False


class OrganSettingValidate(pydantic.BaseModel):
    groups: list["SettingGroupValidate"]


class QueryBody(pydantic.BaseModel):
    user_id: int
    is_admin: bool = False
    request_id: typing.Optional[str | None] = None


class QueryNewsPaperSetting(pydantic.BaseModel):
    user_id: int
    is_admin: bool = False
    request_id: typing.Optional[str | None] = None
    parametrs: dict[str, typing.Any]


class QueryNewsPaperSettingDefault(pydantic.BaseModel):
    user_id: int
    is_admin: bool = False
    request_id: typing.Optional[str | None] = None
    to_default: "OrganSettingDefault"


class QueryOrganSetting(pydantic.BaseModel):
    user_id: int
    is_admin: bool = False
    request_id: typing.Optional[str | None] = None
    parametrs: dict[str, typing.Any]


class QueryOrganSettingDefault(pydantic.BaseModel):
    user_id: int
    is_admin: bool = False
    request_id: typing.Optional[str | None] = None
    to_default: "OrganSettingDefault"


class QueryUserUpdate(pydantic.BaseModel):
    user_id: int
    is_admin: bool = False
    request_id: typing.Optional[str | None] = None
    telegram: typing.Optional[typing.Union["TelegramBody", None]] = None


class ReaderInfo(pydantic.BaseModel):
    news_paper_name: str | None
    news_paper_id: int | None
    rank: int | None
    rank_name: str | None


class Sequence(pydantic.BaseModel):
    seq: str
    number: int
    path: str
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None


class SettingGroupValidate(pydantic.BaseModel):
    tag: str
    name: str
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None
    description: typing.Optional[str | None] = None
    parametrs: list["SettingParametrValidate"]


class SettingParametrValidate(pydantic.BaseModel):
    tag: str
    name: str
    group: str
    type_: str = pydantic.Field(alias="type")
    emodzi: typing.Optional[str | None] = None
    custom_emodzi_id: typing.Optional[str | None] = None
    description: typing.Optional[str | None] = None
    value: typing.Optional[bool | str | int | dict[str, typing.Any] | None] = None
    is_default_value: bool
    is_redact: bool = True
    is_hidden: bool = False

    model_config = pydantic.ConfigDict(populate_by_name=True)


class TelegramBody(pydantic.BaseModel):
    tg_id: int
    username: typing.Optional[str | None] = None
    fullname: typing.Optional[str | None] = None


class ValidationError(pydantic.BaseModel):
    loc: list[str | int]
    msg: str
    type_: str = pydantic.Field(alias="type")
    input: typing.Optional[typing.Any] = None
    ctx: typing.Optional[dict[str, typing.Any]] = None

    model_config = pydantic.ConfigDict(populate_by_name=True)


class AppValidateApiNewspaperAnswerredactrank(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    news_paper: "NewsPaperInfo"
    new_rank: int
    old_rank: int


class AppValidateApiOrganAnswerredactrank(pydantic.BaseModel):
    user: "AnswerUserBody"
    purpose: typing.Optional[typing.Union["AnswerUserBody", None]] = None
    new_rank: int
    old_rank: int


class LogsFileGet200Response(pydantic.BaseModel):
    pass

def get_subclasses_from_same_file() -> list[typing.Type[pydantic.BaseModel]]:
    """
    Due to how Python declares classes in a module,
    we need to update_forward_refs for all the schemas generated
    here in the situation where there are nested classes.
    """
    calling_frame = inspect.currentframe()
    if not calling_frame:
        return []
    else:
        calling_frame = calling_frame.f_back
    module = inspect.getmodule(calling_frame)

    subclasses = []
    for _, c in inspect.getmembers(module):
        if inspect.isclass(c) and issubclass(c, pydantic.BaseModel) and c != pydantic.BaseModel:
            subclasses.append(c)

    return subclasses


subclasses: list[typing.Type[pydantic.BaseModel]] = get_subclasses_from_same_file()
for c in subclasses:
    c.model_rebuild()