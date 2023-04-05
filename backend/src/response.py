from fastapi import HTTPException
from typing import Union


def success(data: Union = None):
    return {"code": 200, "data": data}


def error(err):
    return HTTPException(status_code=err.code, detail=err.message)
