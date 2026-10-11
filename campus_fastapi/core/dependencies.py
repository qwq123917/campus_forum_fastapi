"""公共依赖项 — 鉴权、数据库、Redis 等"""

import redis.asyncio as aioredis
from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.exceptions import BusinessException
from campus_fastapi.core.responses import ResponseCode
from campus_fastapi.core.session import get_session_user_id
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.infrastructure.redis import get_redis
from campus_fastapi.models.user import User


async def get_current_user_id(
    x_session_id: str = Header(..., alias="X-Session-Id"),
    redis: aioredis.Redis = Depends(get_redis),
) -> int:
    """从请求头获取当前用户ID"""
    user_id = await get_session_user_id(redis, x_session_id)
    if user_id is None:
        raise BusinessException(message="未登录或会话已过期", code=ResponseCode.AUTH_ERROR)
    return user_id


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取当前用户 ORM 对象"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise BusinessException(message="用户不存在", code=ResponseCode.NOT_FOUND)
    return user