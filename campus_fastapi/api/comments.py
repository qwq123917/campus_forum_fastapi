"""评论相关路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.dependencies import get_current_user_id
from campus_fastapi.core.responses import success
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.schemas.comments import CommentCreateRequest
from campus_fastapi.services import comment_service

router = APIRouter(prefix="/api", tags=["评论"])


# ========== 帖子评论列表 ==========
@router.get("/posts/{post_id}/comments", summary="获取帖子评论")
async def get_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """获取帖子评论列表"""
    data = await comment_service.get_comments(db, post_id, page, page_size)
    return success(data=data)


# ========== 发表评论 ==========
@router.post("/posts/{post_id}/comments", summary="发表评论")
async def create_comment(
    post_id: int,
    req: CommentCreateRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """发表评论"""
    data = await comment_service.create_comment(db, post_id, req, user_id)
    return success(data=data, message="评论成功")