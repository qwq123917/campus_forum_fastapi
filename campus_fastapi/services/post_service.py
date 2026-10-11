"""帖子业务逻辑层"""

from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.exceptions import BusinessException
from campus_fastapi.core.responses import ResponseCode
from campus_fastapi.repositories import post_repo, user_repo
from campus_fastapi.schemas.posts import PostCreateRequest, PostOut
from campus_fastapi.schemas.common import PaginatedResponse


async def build_post_out(db: AsyncSession, p) -> PostOut:
    """构建帖子输出对象"""
    category_name = await post_repo.get_category_name(db, p.category_id)
    username = await user_repo.get_username(db, p.user_id)

    return PostOut(
        id=p.id,
        title=p.title,
        content=p.content,
        category_id=p.category_id,
        category_name=category_name,
        user_id=p.user_id,
        username=username,
        view_count=p.view_count,
        like_count=p.like_count,
        comment_count=p.comment_count,
        is_top=p.is_top,
        created_at=str(p.created_at) if p.created_at else None,
        updated_at=str(p.updated_at) if p.updated_at else None,
    )


async def get_post_list(db: AsyncSession, page: int, page_size: int,
                        category_id: int | None = None) -> dict:
    """获取帖子列表（分页）"""
    total = await post_repo.count(db, category_id)
    posts = await post_repo.get_list(db, page, page_size, category_id)

    items = []
    for p in posts:
        post_out = await build_post_out(db, p)
        items.append(post_out.model_dump())

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size).model_dump()


async def get_post_detail(db: AsyncSession, post_id: int) -> dict:
    """获取帖子详情"""
    p = await post_repo.get_by_id(db, post_id)
    if not p:
        raise BusinessException(message="帖子不存在", code=ResponseCode.NOT_FOUND)

    # 增加浏览次数
    await post_repo.increment_view_count(db, p)

    post_out = await build_post_out(db, p)
    return post_out.model_dump()


async def create_post(db: AsyncSession, req: PostCreateRequest, user_id: int) -> dict:
    """创建帖子"""
    post = await post_repo.create(db, req.title, req.content, req.category_id, user_id)
    return {"id": post.id}


async def delete_post(db: AsyncSession, post_id: int, user_id: int) -> None:
    """删除帖子（软删除）"""
    p = await post_repo.get_by_id(db, post_id)
    if not p:
        raise BusinessException(message="帖子不存在", code=ResponseCode.NOT_FOUND)
    if p.user_id != user_id:
        raise BusinessException(message="无权删除他人帖子", code=ResponseCode.FAIL)

    await post_repo.soft_delete(db, p)