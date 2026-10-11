"""点赞业务逻辑层"""

from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.repositories import like_repo
from campus_fastapi.schemas.likes import LikeRequest


async def toggle_like(db: AsyncSession, req: LikeRequest, user_id: int) -> dict:
    """点赞或取消点赞"""
    target_type = 1 if req.target_type == "post" else 2

    existing = await like_repo.find_existing(db, user_id, req.target_id, target_type)

    if existing:
        # 取消点赞
        await like_repo.delete(db, existing)
        await like_repo.update_target_count(db, req.target_id, target_type, -1)
        return {"liked": False}
    else:
        # 点赞
        await like_repo.create(db, user_id, req.target_id, target_type)
        await like_repo.update_target_count(db, req.target_id, target_type, +1)
        return {"liked": True}