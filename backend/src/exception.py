import re
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from .errors import ErrorBase, ERROR_NOT_FOUND, ERROR_PARAMETER_ERROR


def set_exceptions(app: FastAPI):
    # 重写 HTTPException 返回类型
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handle(request: Request, exception: StarletteHTTPException):
        if exception.status_code == 404:
            err = ERROR_NOT_FOUND
        else:
            err = ErrorBase(code=exception.status_code, message=exception.detail)
        return JSONResponse(
            status_code=err.code if err.code < 1000 else 200,
            content={"code": err.code, "message": err.message}
        )

    # 重写 RequestValidationError 返回类型
    @app.exception_handler(RequestValidationError)
    async def http_exception_handle(request: Request, exception: RequestValidationError):
        err = ERROR_PARAMETER_ERROR
        return JSONResponse(
            status_code=err.code,
            content={"code": err.code, "message": err.message}
        )
