import uuid

import redis.asyncio as aioredis

from campus_fastapi.core.config import get_settings

settings = get_settings()


async def create_session(redis: aioredis.Redis, user_id: int) -> str:
    """创建Session，返回session_id（UUID格式token）"""
    session_id = str(uuid.uuid4())
    key = f"session:{session_id}"
    await redis.setex(key, settings.SESSION_EXPIRE_SECONDS, str(user_id))
    return session_id


async def get_session_user_id(redis: aioredis.Redis, session_id: str) -> int | None:
    """根据session_id获取user_id"""
    key = f"session:{session_id}"
    user_id_str = await redis.get(key)
    if user_id_str is None:
        return None
    return int(user_id_str)


async def delete_session(redis: aioredis.Redis, session_id: str) -> None:
    """删除Session"""
    key = f"session:{session_id}"
    await redis.delete(key)


async def refresh_session(redis: aioredis.Redis, session_id: str) -> None:
    """刷新Session过期时间"""
    key = f"session:{session_id}"
    await redis.expire(key, settings.SESSION_EXPIRE_SECONDS)