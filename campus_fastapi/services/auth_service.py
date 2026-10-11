"""认证业务逻辑层"""

import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.exceptions import BusinessException
from campus_fastapi.core.responses import ResponseCode
from campus_fastapi.core.security import hash_password, verify_password
from campus_fastapi.core.session import create_session, delete_session
from campus_fastapi.repositories import user_repo
from campus_fastapi.schemas.user import RegisterRequest, LoginRequest, UserInfo, LoginResponse


async def build_user_info(db: AsyncSession, user) -> UserInfo:
    """从 User ORM 对象构建 UserInfo"""
    role_name = await user_repo.get_role_name(db, user.role_id)
    return UserInfo(
        id=user.id,
        username=user.nickname or user.phone or user.email or "",
        phone=user.phone,
        email=user.email,
        nickname=user.nickname,
        avatar=user.avatar,
        role_id=user.role_id,
        role_name=role_name,
        created_at=str(user.created_at) if user.created_at else None,
    )


async def register(db: AsyncSession, redis: aioredis.Redis, req: RegisterRequest) -> dict:
    """用户注册"""
    # 检查手机号是否已注册
    if req.phone:
        existing = await user_repo.get_by_phone(db, req.phone)
        if existing:
            raise BusinessException(message="该手机号已注册", code=ResponseCode.FAIL)

    # 检查邮箱是否已注册
    if req.email:
        existing = await user_repo.get_by_email(db, req.email)
        if existing:
            raise BusinessException(message="该邮箱已注册", code=ResponseCode.FAIL)

    # 创建用户
    user = await user_repo.create(
        db, phone=req.phone, email=req.email,
        password=hash_password(req.password), nickname=req.nickname,
    )

    # 创建Session
    session_id = await create_session(redis, user.id)
    user_info = await build_user_info(db, user)

    return LoginResponse(session_id=session_id, user=user_info).model_dump()


async def login(db: AsyncSession, redis: aioredis.Redis, req: LoginRequest) -> dict:
    """用户登录"""
    # 根据手机号或邮箱查找用户
    if req.phone:
        user = await user_repo.get_by_phone(db, req.phone)
    elif req.email:
        user = await user_repo.get_by_email(db, req.email)
    else:
        raise BusinessException(message="手机号和邮箱至少填写一项", code=ResponseCode.PARAM_ERROR)

    if not user:
        raise BusinessException(message="用户不存在", code=ResponseCode.AUTH_ERROR)

    if not user.is_active:
        raise BusinessException(message="账号已被禁用", code=ResponseCode.AUTH_ERROR)

    # 验证密码
    if not verify_password(req.password, user.password):
        raise BusinessException(message="密码错误", code=ResponseCode.AUTH_ERROR)

    # 创建Session
    session_id = await create_session(redis, user.id)
    user_info = await build_user_info(db, user)

    return LoginResponse(session_id=session_id, user=user_info).model_dump()


async def logout(redis: aioredis.Redis, session_id: str) -> None:
    """用户登出"""
    await delete_session(redis, session_id)


async def get_profile(db: AsyncSession, user_id: int) -> dict:
    """获取当前用户信息"""
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise BusinessException(message="用户不存在", code=ResponseCode.NOT_FOUND)
    user_info = await build_user_info(db, user)
    return user_info.model_dump()