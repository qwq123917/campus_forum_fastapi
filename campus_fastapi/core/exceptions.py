import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from campus_fastapi.core.responses import ResponseCode
from campus_fastapi.core.logging import get_logger

logger = get_logger()


class BusinessException(Exception):
    """业务异常"""

    def __init__(self, message: str = "fail", code: int = ResponseCode.FAIL, data: None = None):
        self.message = message
        self.code = code
        self.data = data


async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    """业务异常处理器"""
    return JSONResponse(
        status_code=200,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """参数校验异常处理器"""
    errors = exc.errors()
    first_error = errors[0] if errors else {}
    message = first_error.get("msg", "参数校验失败")
    return JSONResponse(
        status_code=200,
        content={
            "code": ResponseCode.PARAM_ERROR,
            "message": f"参数校验失败: {message}",
            "data": None,
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理器 - 未知的错误返回500"""
    traceback.print_exc()
    logger.error(f"未处理异常: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "code": ResponseCode.FAIL,
            "message": "服务器开小差了~",
            "data": None,
        },
    )