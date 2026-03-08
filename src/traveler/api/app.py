"""FastAPI 应用 - 旅行规划 API 服务"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from traveler.api.routes import router
from traveler.config.logging import setup_logging
from traveler.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    setup_logging()
    settings = get_settings()
    logger.info("🚀 {} 启动中... (env={})", settings.app_name, settings.app_env)
    yield
    logger.info("👋 {} 已关闭", settings.app_name)


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="企业级旅游规划智能体 API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(router, prefix="/api/v1")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "app": settings.app_name}

    return app
