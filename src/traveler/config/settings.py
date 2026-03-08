"""应用配置 - 使用 pydantic-settings 管理环境变量与配置项"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "data"

class Settings(BaseSettings):
    """全局配置，从 .env 自动加载"""

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---------- App ----------
    app_name: str = "Traveler"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    log_level: str = "DEBUG"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ---------- LLM ----------
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_model_provider: Literal["openai", "anthropic", "deepseek"] = "openai"
    default_model_id: str = "gpt-4o"

    # ---------- Database ----------
    database_url: str = f"sqlite:///{DATA_DIR}/traveler.db"

    # ---------- Vector DB ----------
    vector_db_provider: Literal["chroma", "lancedb", "pgvector"] = "chroma"
    vector_db_path: str = str(DATA_DIR / "chromadb")

    # ---------- MCP ----------
    brave_api_key: str = ""
    google_api_key: str = Field(default="", validation_alias=AliasChoices("GOOGLE_API_KEY", "X_GOOG_API_KEY"))

    # ---------- External APIs ----------
    amadeus_api_key: str = ""
    amadeus_api_secret: str = ""

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

@lru_cache
def get_settings() -> Settings:
    """获取全局配置（单例模式）"""
    return Settings()

