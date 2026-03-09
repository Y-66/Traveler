"""住宿顾问智能体 - 使用酒店搜索 MCP 推荐住宿方案"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agno.agent import Agent
from agno.skills import LocalSkills, Skills

from traveler.agents.prompts import ACCOMMODATION_ADVISOR_INSTRUCTIONS
from traveler.core.database import get_agent_db
from traveler.core.model_factory import create_model

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def create_accommodation_advisor(
    provider: str | None = None,
    model_id: str | None = None,
    mcp_tools: dict[str, Any] | None = None,
) -> Agent:
    """创建住宿顾问智能体

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        mcp_tools: MCP 工具字典 {"hotel_search": tool, ...}
    """
    model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()

    tools: list = []
    if mcp_tools:
        tool = mcp_tools.get("hotel_search")
        if tool:
            tools.append(tool)

    skills = Skills(loaders=[LocalSkills(str(SKILLS_DIR / "local-expert"))])

    return Agent(
        name="AccommodationAdvisor",
        role="住宿顾问，使用酒店搜索工具推荐合适的住宿方案",
        model=model,
        instructions=ACCOMMODATION_ADVISOR_INSTRUCTIONS,
        tools=tools,
        skills=skills,
        db=db,
        markdown=True,
    )
