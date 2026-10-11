"""点赞相关路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.dependencies import get_current_user_id
from campus_fastapi.core.responses import success
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.schemas.likes import LikeRequest
from campus_fastapi.services import like_service

router = APIRouter(prefix="/api", tags=["点赞"])


# ========== 点赞/取消点赞 ==========
@router.post("/likes", summary="点赞/取消点赞")
async def toggle_like(
    req: LikeRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """点赞或取消点赞"""
    data = await like_service.toggle_like(db, req, user_id)
    message = "取消点赞" if not data["liked"] else "点赞成功"
    return success(data=data, message=message)