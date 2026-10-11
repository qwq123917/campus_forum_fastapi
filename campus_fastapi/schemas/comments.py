from pydantic import BaseModel


class CommentCreateRequest(BaseModel):
    """创建评论请求"""
    content: str
    parent_id: int | None = None


class CommentOut(BaseModel):
    """评论输出"""
    id: int
    post_id: int
    user_id: int
    username: str | None = None
    content: str
    parent_id: int | None = None
    like_count: int = 0
    created_at: str | None = None

    model_config = {"from_attributes": True}