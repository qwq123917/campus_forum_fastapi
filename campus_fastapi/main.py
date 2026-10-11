"""
Campus FastAPI 入口文件

启动方式:
    uvicorn campus_fastapi.main:app --reload
"""

from campus_fastapi.app.app_factory import create_app

app = create_app()

__all__ = ["app"]