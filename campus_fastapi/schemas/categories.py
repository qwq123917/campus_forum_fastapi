from pydantic import BaseModel


class CategoryOut(BaseModel):
    """分类输出"""
    id: int
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}