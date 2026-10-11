from sqlalchemy import String, Text, DateTime, func, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class Post(Base):
    __tablename__ = "sys_post"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="帖子ID"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="发帖用户ID"
    )
    category_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("sys_category.id"), nullable=True, comment="分类ID"
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="帖子标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="帖子内容")
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览次数")
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="点赞数")
    comment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="评论数")
    is_top: Mapped[bool] = mapped_column(default=False, nullable=False, comment="是否置顶")
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, comment="是否删除")
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间"
    )