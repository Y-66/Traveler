"""路线规划智能体 - 使用 Google Maps MCP 规划路线和交通方案"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agno.agent import Agent
from agno.skills import LocalSkills, Skills

from traveler.agents.prompts import ROUTE_PLANNER_INSTRUCTIONS
from traveler.core.database import get_agent_db
from traveler.core.model_factory import create_model

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def create_route_planner(
    provider: str | None = None,
    model_id: str | None = None,
    mcp_tools: dict[str, Any] | None = None,
) -> Agent:
    """创建路线规划智能体

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        mcp_tools: MCP 工具字典 {"google_maps": tool, ...}
    """
    model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()

    tools: list = []
    if mcp_tools:
        tool = mcp_tools.get("google_maps")
        if tool:
            tools.append(tool)

    skills = Skills(loaders=[LocalSkills(str(SKILLS_DIR / "travel-planning"))])

    return Agent(
        name="RoutePlanner",
        role="路线规划专家，使用地图工具规划路线和交通方案",
        model=model,
        instructions=ROUTE_PLANNER_INSTRUCTIONS,
        tools=tools,
        skills=skills,
        db=db,
        markdown=True,
    )
