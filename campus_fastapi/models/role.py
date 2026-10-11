from sqlalchemy import String, DateTime, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class Role(Base):
    __tablename__ = "sys_role"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="角色ID"
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="角色名称")
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="角色编码")
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="角色描述")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, comment="是否启用")
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间"
    )