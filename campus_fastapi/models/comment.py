from sqlalchemy import String, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class Comment(Base):
    __tablename__ = "sys_comment"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="评论ID"
    )
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_post.id"), nullable=False, comment="帖子ID"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="评论用户ID"
    )
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("sys_comment.id"), nullable=True, comment="父评论ID"
    )
    content: Mapped[str] = mapped_column(String(1000), nullable=False, comment="评论内容")
    like_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False, comment="点赞数")
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, comment="是否删除")
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间"
    )