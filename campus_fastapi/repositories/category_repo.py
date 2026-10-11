"""分类数据访问层"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.models.category import Category


async def get_active_list(db: AsyncSession) -> list[Category]:
    """获取所有启用的分类"""
    stmt = select(Category).where(Category.is_active == True).order_by(Category.sort_order)  # noqa: E712
    result = await db.execute(stmt)
    return result.scalars().all()