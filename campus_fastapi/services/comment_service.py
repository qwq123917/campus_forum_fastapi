"""评论业务逻辑层"""

from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.exceptions import BusinessException
from campus_fastapi.core.responses import ResponseCode
from campus_fastapi.repositories import post_repo, comment_repo, user_repo
from campus_fastapi.schemas.comments import CommentCreateRequest, CommentOut
from campus_fastapi.schemas.common import PaginatedResponse


async def get_comments(db: AsyncSession, post_id: int,
                       page: int, page_size: int) -> dict:
    """获取帖子评论列表"""
    total = await comment_repo.count_by_post(db, post_id)
    comments = await comment_repo.get_list_by_post(db, post_id, page, page_size)

    items = []
    for c in comments:
        username = await user_repo.get_username(db, c.user_id)
        items.append(CommentOut(
            id=c.id,
            post_id=c.post_id,
            user_id=c.user_id,
            username=username,
            content=c.content,
            parent_id=c.parent_id,
            like_count=c.like_count,
            created_at=str(c.created_at) if c.created_at else None,
        ))

    return PaginatedResponse(
        items=[i.model_dump() for i in items],
        total=total, page=page, page_size=page_size,
    ).model_dump()


async def create_comment(db: AsyncSession, post_id: int,
                         req: CommentCreateRequest, user_id: int) -> dict:
    """发表评论"""
    # 检查帖子是否存在
    post = await post_repo.get_by_id(db, post_id)
    if not post:
        raise BusinessException(message="帖子不存在", code=ResponseCode.NOT_FOUND)

    comment = await comment_repo.create(
        db, post_id=post_id, user_id=user_id,
        content=req.content, parent_id=req.parent_id,
    )

    # 更新帖子评论数
    await comment_repo.increment_post_comment_count(db, post)

    return {"id": comment.id}