"""认证相关路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import redis.asyncio as aioredis

from campus_fastapi.core.dependencies import get_current_user_id
from campus_fastapi.core.responses import success
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.infrastructure.redis import get_redis
from campus_fastapi.schemas.user import RegisterRequest, LoginRequest
from campus_fastapi.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", summary="用户注册")
async def register(
    req: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    """用户注册 - 支持手机号或邮箱注册"""
    data = await auth_service.register(db, redis, req)
    return success(data=data, message="注册成功")


@router.post("/login", summary="用户登录")
async def login(
    req: LoginRequest,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    """用户登录 - 支持手机号或邮箱登录"""
    data = await auth_service.login(db, redis, req)
    return success(data=data, message="登录成功")


@router.post("/logout", summary="用户登出")
async def logout(
    session_id: str,
    redis: aioredis.Redis = Depends(get_redis),
):
    """用户登出"""
    await auth_service.logout(redis, session_id)
    return success(message="登出成功")


@router.post("/profile", summary="获取当前用户信息")
async def get_profile(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取当前登录用户信息"""
    data = await auth_service.get_profile(db, user_id)
    return success(data=data)