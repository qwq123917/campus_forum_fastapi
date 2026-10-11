"""评论数据访问层"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.models.comment import Comment
from campus_fastapi.models.post import Post


async def count_by_post(db: AsyncSession, post_id: int) -> int:
    """统计帖子评论数量"""
    conditions = [Comment.post_id == post_id, Comment.is_deleted == False]  # noqa: E712
    stmt = select(func.count()).select_from(Comment).where(*conditions)
    return (await db.execute(stmt)).scalar() or 0


async def get_list_by_post(db: AsyncSession, post_id: int,
                           page: int, page_size: int) -> list[Comment]:
    """获取帖子评论列表（分页）"""
    conditions = [Comment.post_id == post_id, Comment.is_deleted == False]  # noqa: E712
    stmt = (
        select(Comment)
        .where(*conditions)
        .order_by(Comment.created_at.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create(db: AsyncSession, post_id: int, user_id: int,
                 content: str, parent_id: int | None = None) -> Comment:
    """创建评论"""
    comment = Comment(post_id=post_id, user_id=user_id, content=content, parent_id=parent_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def increment_post_comment_count(db: AsyncSession, post: Post) -> None:
    """增加帖子评论计数"""
    post.comment_count += 1
    await db.commit()