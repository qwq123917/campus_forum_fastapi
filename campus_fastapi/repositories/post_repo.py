"""帖子数据访问层"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.models.post import Post
from campus_fastapi.models.category import Category


async def get_by_id(db: AsyncSession, post_id: int) -> Post | None:
    """根据ID获取帖子（未删除）"""
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.is_deleted == False)  # noqa: E712
    )
    return result.scalar_one_or_none()


async def count(db: AsyncSession, category_id: int | None = None) -> int:
    """统计帖子数量"""
    conditions = [Post.is_deleted == False]  # noqa: E712
    if category_id is not None:
        conditions.append(Post.category_id == category_id)
    stmt = select(func.count()).select_from(Post).where(*conditions)
    return (await db.execute(stmt)).scalar() or 0


async def get_list(db: AsyncSession, page: int, page_size: int,
                   category_id: int | None = None) -> list[Post]:
    """获取帖子列表（分页）"""
    conditions = [Post.is_deleted == False]  # noqa: E712
    if category_id is not None:
        conditions.append(Post.category_id == category_id)
    stmt = (
        select(Post)
        .where(*conditions)
        .order_by(Post.is_top.desc(), Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_category_name(db: AsyncSession, category_id: int | None) -> str | None:
    """获取分类名"""
    if not category_id:
        return None
    result = await db.execute(select(Category.name).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, title: str, content: str,
                 category_id: int | None, user_id: int) -> Post:
    """创建帖子"""
    post = Post(title=title, content=content, category_id=category_id, user_id=user_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def soft_delete(db: AsyncSession, post: Post) -> None:
    """软删除帖子"""
    post.is_deleted = True
    await db.commit()


async def increment_view_count(db: AsyncSession, post: Post) -> None:
    """增加浏览次数"""
    post.view_count += 1
    await db.commit()
    await db.refresh(post)