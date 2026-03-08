"""LLM 模型工厂 - 根据配置动态创建模型实例"""

from __future__ import annotations

from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat

from traveler.config.settings import get_settings


def create_model(
    provider: str | None = None,
    model_id: str | None = None,
):
    """根据 provider 创建对应的 LLM 模型实例

    Args:
        provider: 模型提供商 (openai / anthropic / deepseek)
        model_id: 模型 ID
    """
    settings = get_settings()
    provider = provider or settings.default_model_provider
    model_id = model_id or settings.default_model_id

    match provider:
        case "openai":
            return OpenAIChat(
                id=model_id,
                api_key=settings.openai_api_key or None,
            )
        case "anthropic":
            return Claude(
                id=model_id,
                api_key=settings.anthropic_api_key or None,
            )
        case "deepseek":
            return OpenAIChat(
                id=model_id,
                api_key=settings.openai_api_key or None,
                base_url="https://api.deepseek.com",
            )
        case _:
            raise ValueError(f"不支持的模型提供商: {provider}")
