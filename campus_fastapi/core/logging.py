"""日志配置"""

import logging


def setup_logging() -> None:
    """配置应用日志"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def get_logger(name: str = "campus_fastapi") -> logging.Logger:
    """获取日志器"""
    return logging.getLogger(name)