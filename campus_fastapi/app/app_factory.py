"""
Campus FastAPI 应用工厂

用法:
    # 在 main.py 中
    from campus_fastapi.app.app_factory import create_app
    app = create_app()

    # 或直接使用模块级实例
    from campus_fastapi.app import app
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from campus_fastapi.api.auth import router as auth_router
from campus_fastapi.api.posts import router as posts_router
from campus_fastapi.api.comments import router as comments_router
from campus_fastapi.api.likes import router as likes_router
from campus_fastapi.api.categories import router as categories_router
from campus_fastapi.api.chat import router as chat_router
from campus_fastapi.core.logging import setup_logging, get_logger
from campus_fastapi.core.config import get_settings
from campus_fastapi.core.exceptions import (
    BusinessException,
    business_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)
from campus_fastapi.infrastructure.database import engine, Base
from campus_fastapi.infrastructure.redis import close_redis

# 显式导入所有模型，确保 SQLAlchemy metadata 注册
import campus_fastapi.models.user
import campus_fastapi.models.role
import campus_fastapi.models.post
import campus_fastapi.models.comment
import campus_fastapi.models.like
import campus_fastapi.models.category
import campus_fastapi.models.chat

# 配置日志
setup_logging()
logger = get_logger()


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例"""
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """应用生命周期 — 启动与关闭"""
        print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 正在启动...")
        # 启动时创建数据库表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f"✅ 数据库初始化完成")
        print(f"✅ {settings.APP_NAME} 启动成功！")
        yield
        # 关闭时清理资源
        print(f"🛑 {settings.APP_NAME} 正在关闭...")
        await close_redis()
        await engine.dispose()
        print(f"🛑 资源清理完成")

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    # 注册异常处理器
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # 注册路由
    app.include_router(auth_router)
    app.include_router(posts_router)
    app.include_router(comments_router)
    app.include_router(likes_router)
    app.include_router(categories_router)
    app.include_router(chat_router)

    # 健康检查
    @app.get("/", summary="健康检查")
    async def health_check():
        return {"code": 0, "message": "success", "data": f"{settings.APP_NAME} is running"}

    return app