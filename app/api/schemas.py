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


class AnswerAllPathInfo(pydantic.BaseModel):
    paths: list["AnswerPathInfo"] | None


class AnswerAllSeqInfo(pydantic.BaseModel):
    seqs: list["AnswerSeqInfo"] | None


class AnswerBaseInfo(pydantic.BaseModel):
    tg_id: int
    name: typing.Optional[str | None] = None
    username: typing.Optional[str | None] = None
    path_name: typing.Optional[str | None] = None
    seq: typing.Optional[int | None] = None
    seq_name: typing.Optional[str | None] = None
    titul: typing.Optional[str | None] = None
    organ_name: typing.Optional[str | None] = None
    rank: typing.Optional[int | None] = None
    rank_name: typing.Optional[str | None] = None


class AnswerGAFullInfo(pydantic.BaseModel):
    ga_name: str | None
    paths: list["AnswerPathInfo"] | None


class AnswerGAInfo(pydantic.BaseModel):
    group: str
    name: str
    ga_id: int


class AnswerGASearchInfo(pydantic.BaseModel):
    search_value: str | None
    gas: list["AnswerGAInfo"] | None


class AnswerGroupInfo(pydantic.BaseModel):
    group_name: str | None
    gas: list["AnswerGAInfo"] | None


class AnswerPathFullInfo(pydantic.BaseModel):
    ga_name: str | None
    seqs: list["AnswerSeqInfo"] | None
    name: str | None


class AnswerPathInfo(pydantic.BaseModel):
    group: str
    name: str
    path_id: int


class AnswerPathSearchInfo(pydantic.BaseModel):
    search_value: str | None
    paths: list["AnswerPathInfo"] | None


class AnswerRedactSeq(pydantic.BaseModel):
    tg_id: int
    old: typing.Optional[typing.Union["Data", None]] = None
    new: typing.Optional[typing.Union["Data", None]] = None
    operation: str


class AnswerSeqInfo(pydantic.BaseModel):
    seq: int
    name: str
    path_id: int
    seq_id: int


class AnswerSeqSearchInfo(pydantic.BaseModel):
    search_value: str | None
    seqs: list["AnswerPathInfo"] | None


class AnswerTimeInfo(pydantic.BaseModel):
    tg_id: int
    next_upseq: str | None
    last_upseq: str
    upseq_days: int | None


class AnswerTimeRedact(pydantic.BaseModel):
    tg_id: int
    old_time: str
    new_time: str
    seconds: int
    operator: str


class AnswerTimeReplace(pydantic.BaseModel):
    tg_id: int
    old_time: str
    new_time: str


class AnswerUserBody(pydantic.BaseModel):
    tg_id: int


class BaseExceptionResponse(pydantic.BaseModel):
    message: str
    status_code: int
    headers: typing.Optional[dict[str, typing.Any] | None] = None
    content: typing.Optional[typing.Any] = None


class Data(pydantic.BaseModel):
    seq: str
    number: int
    path: str


class HTTPValidationError(pydantic.BaseModel):
    detail: list["ValidationError"]


class QueryBody(pydantic.BaseModel):
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


class Endpoint200Response(pydantic.BaseModel):
    pass

class Main200Response(pydantic.BaseModel):
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