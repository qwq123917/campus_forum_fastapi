"""帖子相关路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.dependencies import get_current_user_id
from campus_fastapi.core.responses import success
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.schemas.posts import PostCreateRequest
from campus_fastapi.services import post_service

router = APIRouter(prefix="/api", tags=["帖子"])


# ========== 帖子列表 ==========
@router.get("/posts", summary="获取帖子列表")
async def get_post_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取帖子列表（分页）"""
    data = await post_service.get_post_list(db, page, page_size, category_id)
    return success(data=data)


# ========== 帖子详情 ==========
@router.get("/posts/{post_id}", summary="获取帖子详情")
async def get_post_detail(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取帖子详情"""
    data = await post_service.get_post_detail(db, post_id)
    return success(data=data)


# ========== 创建帖子 ==========
@router.post("/posts", summary="创建帖子")
async def create_post(
    req: PostCreateRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """创建帖子"""
    data = await post_service.create_post(db, req, user_id)
    return success(data=data, message="发帖成功")


# ========== 删除帖子 ==========
@router.delete("/posts/{post_id}", summary="删除帖子")
async def delete_post(
    post_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除帖子（软删除）"""
    await post_service.delete_post(db, post_id, user_id)
    return success(message="删除成功")