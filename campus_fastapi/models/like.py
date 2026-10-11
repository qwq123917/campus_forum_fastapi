from sqlalchemy import DateTime, func, BigInteger, SmallInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class Like(Base):
    __tablename__ = "sys_like"
    __table_args__ = (
        UniqueConstraint("user_id", "target_id", "target_type", name="uk_user_target"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="点赞ID"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="用户ID"
    )
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="目标ID")
    target_type: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, comment="目标类型 1-帖子 2-评论"
    )
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )