from sqlalchemy import String, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="用户ID"
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_role.id"), default=2, nullable=False, comment="角色ID，默认普通用户"
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), unique=True, nullable=True, index=True, comment="手机号"
    )
    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True, index=True, comment="邮箱"
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希")
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="头像URL")
    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False, comment="是否激活"
    )
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间"
    )