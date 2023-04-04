from __future__ import annotations
import math
from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    size: int = Query(15, gt=1, le=500)
    page: int = Query(1, ge=1)

    def to_raw_params(self) -> RawParams:
        return RawParams(limit=self.size, offset=self.size * (self.page - 1))


class Page(AbstractPage[T], Generic[T]):
    code: int
    data: Sequence[T]
    meta: dict

    __params_type__ = Params

    @classmethod
    def create(cls, data: data, total: int, params: Params) -> Page[T]:
        pages = math.ceil(total / params.size)
        return cls(code=200, data=data, meta={
            "pagination": {
                "size": params.size,
                "page": params.page,
                "total": total,
                "pages": pages
            }
        })
