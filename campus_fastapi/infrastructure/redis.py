import redis.asyncio as aioredis

from campus_fastapi.core.config import get_settings

settings = get_settings()

redis_client: aioredis.Redis = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


async def get_redis() -> aioredis.Redis:
    """获取Redis客户端依赖"""
    return redis_client


async def close_redis() -> None:
    """关闭Redis连接"""
    await redis_client.close()