from pydantic import BaseModel


class LikeRequest(BaseModel):
    """点赞请求"""
    target_id: int
    target_type: str  # "post" 或 "comment"