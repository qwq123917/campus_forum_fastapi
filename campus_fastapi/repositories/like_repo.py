"""点赞数据访问层"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.models.like import Like
from campus_fastapi.models.post import Post
from campus_fastapi.models.comment import Comment


async def find_existing(db: AsyncSession, user_id: int,
                        target_id: int, target_type: int) -> Like | None:
    """查找是否已点赞"""
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.target_id == target_id,
        Like.target_type == target_type,
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def create(db: AsyncSession, user_id: int,
                 target_id: int, target_type: int) -> Like:
    """创建点赞记录"""
    like = Like(user_id=user_id, target_id=target_id, target_type=target_type)
    db.add(like)
    await db.commit()
    return like


async def delete(db: AsyncSession, like: Like) -> None:
    """删除点赞记录"""
    await db.delete(like)
    await db.commit()


async def update_target_count(db: AsyncSession, target_id: int,
                              target_type: int, delta: int) -> None:
    """更新目标点赞计数（delta: +1 或 -1）"""
    if target_type == 1:
        await db.execute(
            Post.__table__.update().where(Post.id == target_id)
            .values(like_count=Post.like_count + delta)
        )
    else:
        await db.execute(
            Comment.__table__.update().where(Comment.id == target_id)
            .values(like_count=Comment.like_count + delta)
        )
    await db.commit()