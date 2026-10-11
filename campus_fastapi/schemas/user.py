import re
from typing import Optional

from pydantic import BaseModel, field_validator


class RegisterRequest(BaseModel):
    """注册请求"""
    phone: Optional[str] = None
    email: Optional[str] = None
    password: str
    nickname: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("密码不得低于6位")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is not None and not re.match(r"^1[3-9]\d{9}$", v):
            raise ValueError("手机号格式不正确")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        if v is not None and not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", v):
            raise ValueError("邮箱格式不正确")
        return v

    def model_post_init(self, __context):
        if self.phone is None and self.email is None:
            raise ValueError("手机号和邮箱至少填写一项")


class LoginRequest(BaseModel):
    """登录请求"""
    phone: Optional[str] = None
    email: Optional[str] = None
    password: str

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("密码不能为空")
        return v

    def model_post_init(self, __context):
        if self.phone is None and self.email is None:
            raise ValueError("手机号和邮箱至少填写一项")


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    username: str | None = None
    phone: str | None = None
    email: str | None = None
    nickname: str | None = None
    avatar: str | None = None
    role_id: int = 2
    role_name: str = "普通用户"
    created_at: str | None = None


class LoginResponse(BaseModel):
    """登录响应"""
    session_id: str
    user: UserInfo