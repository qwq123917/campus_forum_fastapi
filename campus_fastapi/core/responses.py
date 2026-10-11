from typing import Any

from fastapi.responses import JSONResponse


class ResponseCode:
    """统一响应码"""
    SUCCESS = 0
    FAIL = 1
    PARAM_ERROR = 2
    AUTH_ERROR = 3
    NOT_FOUND = 4


class UnifiedResponse:
    """统一响应格式"""

    def __init__(self, code: int = ResponseCode.SUCCESS, message: str = "success", data: Any = None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data,
        }


def success(data: Any = None, message: str = "success") -> dict:
    """成功响应"""
    return UnifiedResponse(code=ResponseCode.SUCCESS, message=message, data=data).to_dict()


def fail(message: str = "fail", code: int = ResponseCode.FAIL, data: Any = None) -> dict:
    """失败响应"""
    return UnifiedResponse(code=code, message=message, data=data).to_dict()


def success_response(data: Any = None, message: str = "success") -> JSONResponse:
    """成功响应（JSONResponse）"""
    content = success(data=data, message=message)
    return JSONResponse(content=content)


def fail_response(message: str = "fail", code: int = ResponseCode.FAIL, data: Any = None, status_code: int = 200) -> JSONResponse:
    """失败响应（JSONResponse）"""
    content = fail(message=message, code=code, data=data)
    return JSONResponse(content=content, status_code=status_code)