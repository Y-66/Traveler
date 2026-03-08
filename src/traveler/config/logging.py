"""日志配置 - 基于 loguru 的统一日志系统"""

from __future__ import annotations

import sys

from loguru import logger

from traveler.config.settings import get_settings


def setup_logging() -> None:
    """初始化日志系统"""
    settings = get_settings()

    # 移除默认 handler
    logger.remove()

    # 控制台输出
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # 文件输出（生产环境）
    if settings.is_production:
        logger.add(
            "logs/traveler_{time:YYYY-MM-DD}.log",
            level="INFO",
            rotation="00:00",
            retention="30 days",
            compression="gz",
            encoding="utf-8",
        )

    logger.info("日志系统已初始化 | 级别: {}", settings.log_level)
