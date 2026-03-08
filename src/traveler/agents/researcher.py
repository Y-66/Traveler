"""旅行研究智能体 - 专注于目的地信息收集和分析"""

from __future__ import annotations

from agno.agent import Agent

from traveler.agents.prompts import RESEARCHER_INSTRUCTIONS
from traveler.core.database import get_agent_db
from traveler.core.knowledge import get_travel_knowledge
from traveler.core.model_factory import create_model


def create_researcher(
    provider: str | None = None,
    model_id: str | None = None,
    mcp_tools_list: list | None = None,
) -> Agent:
    """创建旅行研究智能体

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        mcp_tools_list: 已连接的 MCPTools 列表（由调用方管理生命周期）
    """
    model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()
    knowledge = get_travel_knowledge()

    tools: list = []
    if mcp_tools_list:
        tools.extend(mcp_tools_list)

    return Agent(
        name="TravelResearcher",
        role="旅行研究专家，负责搜索和收集目的地信息",
        model=model,
        instructions=RESEARCHER_INSTRUCTIONS,
        tools=tools,
        knowledge=knowledge,
        search_knowledge=True,
        db=db,
        markdown=True,
    )
