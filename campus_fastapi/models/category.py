from sqlalchemy import String, DateTime, func, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class Category(Base):
    __tablename__ = "sys_category"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="分类ID"
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    icon: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="分类图标URL")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序序号")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, comment="是否启用")
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间"
    )