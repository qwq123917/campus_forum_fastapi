"""分类相关路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.responses import success
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.services import category_service

router = APIRouter(prefix="/api", tags=["分类"])


# ========== 分类列表 ==========
@router.get("/categories", summary="获取分类列表")
async def get_category_list(db: AsyncSession = Depends(get_db)):
    """获取所有启用的分类"""
    data = await category_service.get_category_list(db)
    return success(data=data)