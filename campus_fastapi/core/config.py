from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # 应用配置
    APP_NAME: str = "Campus FastAPI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # 数据库配置（独立字段）
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "campus_forum_db"

    # Redis配置（独立字段）
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWD: str = ""

    # Session配置
    SESSION_EXPIRE_SECONDS: int = 86400 * 7  # 7天过期

    # 密码配置
    PASSWORD_MIN_LENGTH: int = 6

    @property
    def DATABASE_URL(self) -> str:
        """根据独立字段构建数据库连接URL"""
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self) -> str:
        """根据独立字段构建Redis连接URL"""
        if self.REDIS_PASSWD:
            return f"redis://:{self.REDIS_PASSWD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()