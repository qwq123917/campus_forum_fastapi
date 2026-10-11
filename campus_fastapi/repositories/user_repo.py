"""用户数据访问层"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.models.user import User
from campus_fastapi.models.role import Role


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    """根据ID获取用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_by_phone(db: AsyncSession, phone: str) -> User | None:
    """根据手机号获取用户"""
    result = await db.execute(select(User).where(User.phone == phone))
    return result.scalar_one_or_none()


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    """根据邮箱获取用户"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_username(db: AsyncSession, user_id: int) -> str:
    """获取用户显示名（昵称 > 手机号 > 匿名）"""
    row = (await db.execute(
        select(User.nickname, User.phone).where(User.id == user_id)
    )).first()
    if not row:
        return "匿名"
    nickname, phone = row
    return nickname or phone or "匿名"


async def get_role_name(db: AsyncSession, role_id: int | None) -> str:
    """获取角色名"""
    if not role_id:
        return "普通用户"
    result = await db.execute(select(Role.name).where(Role.id == role_id))
    return result.scalar_one_or_none() or "普通用户"


async def create(db: AsyncSession, phone: str | None, email: str | None,
                 password: str, nickname: str | None = None) -> User:
    """创建用户"""
    user = User(phone=phone, email=email, password=password, nickname=nickname)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user