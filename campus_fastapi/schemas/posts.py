from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    """创建帖子请求"""
    title: str
    content: str
    category_id: int


class PostOut(BaseModel):
    """帖子输出"""
    id: int
    title: str
    content: str
    category_id: int | None = None
    category_name: str | None = None
    user_id: int
    username: str | None = None
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    is_top: bool = False
    created_at: str | None = None
    updated_at: str | None = None

    model_config = {"from_attributes": True}