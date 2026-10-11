"""分类业务逻辑层"""

from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.repositories import category_repo
from campus_fastapi.schemas.categories import CategoryOut


async def get_category_list(db: AsyncSession) -> list[dict]:
    """获取所有启用的分类"""
    categories = await category_repo.get_active_list(db)
    return [CategoryOut(id=c.id, name=c.name, description=c.icon).model_dump() for c in categories]