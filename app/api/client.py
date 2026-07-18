from __future__ import annotations

import typing

from clientele import api as clientele_api
from . import config, schemas

client = clientele_api.APIClient(config=config.Config())


@client.put("/beyonder/drink", response_map={200: schemas.AnswerRedactSeq, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def drink(result: schemas.AnswerRedactSeq | schemas.BaseExceptionResponse | schemas.HTTPValidationError, data: schemas.QueryBody, tg_id: typing.Optional[int] = None, path_name: typing.Optional[str] = None, seq: typing.Optional[int] = None) -> schemas.AnswerRedactSeq | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Drink
    """
    return result


@client.patch("/beyonder/upseq", response_map={200: schemas.AnswerRedactSeq, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def upseq(result: schemas.AnswerRedactSeq | schemas.BaseExceptionResponse | schemas.HTTPValidationError, data: schemas.QueryBody, tg_id: typing.Optional[int] = None, path_name: typing.Optional[str] = None, seq: typing.Optional[int] = None) -> schemas.AnswerRedactSeq | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Upseq
    """
    return result


@client.patch("/beyonder/downseq", response_map={200: schemas.AnswerRedactSeq, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def dowseq(result: schemas.AnswerRedactSeq | schemas.BaseExceptionResponse | schemas.HTTPValidationError, data: schemas.QueryBody, tg_id: typing.Optional[int] = None, path_name: typing.Optional[str] = None, seq: typing.Optional[int] = None) -> schemas.AnswerRedactSeq | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Dowseq
    """
    return result



@client.get("/beyonder/time/info/{tg_id}", response_map={200: schemas.AnswerTimeInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def time_info(result: schemas.AnswerTimeInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, tg_id: int) -> schemas.AnswerTimeInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Time Info
    """
    return result


@client.patch("/beyonder/time/replace", response_map={200: schemas.AnswerTimeReplace, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def time_replace(result: schemas.AnswerTimeReplace | schemas.BaseExceptionResponse | schemas.HTTPValidationError, data: schemas.QueryBody, date: str, tg_id: typing.Optional[int] = None) -> schemas.AnswerTimeReplace | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Time Replace
    """
    return result


@client.patch("/beyonder/time/redact", response_map={200: schemas.AnswerTimeRedact, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def time_redact(result: schemas.AnswerTimeRedact | schemas.BaseExceptionResponse | schemas.HTTPValidationError, data: schemas.QueryBody, seconds: float, operator: str, tg_id: typing.Optional[int] = None) -> schemas.AnswerTimeRedact | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Time Redact
    """
    return result


@client.post("/beyonder/kill", response_map={200: schemas.AnswerUserBody, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 453: schemas.BaseExceptionResponse, 454: schemas.BaseExceptionResponse, 455: schemas.BaseExceptionResponse, 456: schemas.BaseExceptionResponse, 457: schemas.BaseExceptionResponse})

async def kill(result: schemas.AnswerUserBody | schemas.BaseExceptionResponse | schemas.HTTPValidationError, data: schemas.QueryBody, tg_id: typing.Optional[int] = None) -> schemas.AnswerUserBody | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Kill
    """
    return result



@client.get("/wiki/seq/search", response_map={200: schemas.AnswerSeqSearchInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def search_seq(result: schemas.AnswerSeqSearchInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, value: str) -> schemas.AnswerSeqSearchInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Search Seq
    """
    return result



@client.get("/wiki/seq/all", response_map={200: schemas.AnswerAllSeqInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_seqs(result: schemas.AnswerAllSeqInfo | schemas.BaseExceptionResponse) -> schemas.AnswerAllSeqInfo | schemas.BaseExceptionResponse:
    """Get Seqs

       
    """
    return result



@client.get("/wiki/seq", response_map={200: schemas.AnswerSeqFullInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_seq(result: schemas.AnswerSeqFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, name: typing.Optional[str] = None, id: typing.Optional[int] = None) -> schemas.AnswerSeqFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Seq
    """
    return result



@client.get("/wiki/path/search", response_map={200: schemas.AnswerPathSearchInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def search_path(result: schemas.AnswerPathSearchInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, value: str) -> schemas.AnswerPathSearchInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Search Path
    """
    return result



@client.get("/wiki/path/all", response_map={200: schemas.AnswerAllPathInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_paths(result: schemas.AnswerAllPathInfo | schemas.BaseExceptionResponse) -> schemas.AnswerAllPathInfo | schemas.BaseExceptionResponse:
    """Get Paths

       
    """
    return result



@client.get("/wiki/path", response_map={200: schemas.AnswerPathFullInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_path(result: schemas.AnswerPathFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, name: typing.Optional[str] = None, id: typing.Optional[int] = None) -> schemas.AnswerPathFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Path
    """
    return result



@client.get("/wiki/path/seq", response_map={200: schemas.AnswerSeqFullInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_seq_by_path_id(result: schemas.AnswerSeqFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, path_id: int, seq_number: int) -> schemas.AnswerSeqFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Seq By Path Id
    """
    return result



@client.get("/wiki/path/seqs", response_map={200: schemas.AnswerAllSeqInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_seqs_by_path_id(result: schemas.AnswerAllSeqInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, path_id: int) -> schemas.AnswerAllSeqInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Seqs By Path Id
    """
    return result



@client.get("/wiki/ga/search", response_map={200: schemas.AnswerGASearchInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def search_ga(result: schemas.AnswerGASearchInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, value: str) -> schemas.AnswerGASearchInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Search Ga
    """
    return result



@client.get("/wiki/ga/all", response_map={200: schemas.AnswerAllGAInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_gas(result: schemas.AnswerAllGAInfo | schemas.BaseExceptionResponse) -> schemas.AnswerAllGAInfo | schemas.BaseExceptionResponse:
    """Get Gas

        
    """
    return result



@client.get("/wiki/ga", response_map={200: schemas.AnswerGAFullInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_ga(result: schemas.AnswerGAFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, name: typing.Optional[str] = None, id: typing.Optional[int] = None) -> schemas.AnswerGAFullInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Ga
    """
    return result



@client.get("/wiki/ga/paths", response_map={200: schemas.AnswerAllPathInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_path_by_ga_id(result: schemas.AnswerAllPathInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, ga_id: int) -> schemas.AnswerAllPathInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Path By Ga Id
    """
    return result



@client.get("/wiki/group/all", response_map={200: schemas.AnswerAllGroupInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_groups(result: schemas.AnswerAllGroupInfo | schemas.BaseExceptionResponse) -> schemas.AnswerAllGroupInfo | schemas.BaseExceptionResponse:
    """Get Groups

       
    """
    return result



@client.get("/wiki/group", response_map={200: schemas.AnswerGroupInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError, 433: schemas.BaseExceptionResponse, 434: schemas.BaseExceptionResponse})

async def get_group(result: schemas.AnswerGroupInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, name: str) -> schemas.AnswerGroupInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Group
    """
    return result



@client.get("/stats/info", response_map={200: schemas.Endpoint200Response, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError})

async def endpoint(result: schemas.BaseExceptionResponse | schemas.Endpoint200Response | schemas.HTTPValidationError) -> schemas.BaseExceptionResponse | schemas.Endpoint200Response | schemas.HTTPValidationError:
    """Endpoint
    """
    return result



@client.get("/info/{tg_id}", response_map={200: schemas.AnswerBaseInfo, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse, 422: schemas.HTTPValidationError})

async def get_info(result: schemas.AnswerBaseInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError, tg_id: int) -> schemas.AnswerBaseInfo | schemas.BaseExceptionResponse | schemas.HTTPValidationError:
    """Get Info
    """
    return result



@client.get("/", response_map={200: schemas.AnswerMain, 400: schemas.BaseExceptionResponse, 403: schemas.BaseExceptionResponse})

async def main(result: schemas.AnswerMain | schemas.BaseExceptionResponse) -> schemas.AnswerMain | schemas.BaseExceptionResponse:
    """Main
    """
    return result