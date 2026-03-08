"""旅行规划主智能体 - 单 Agent 模式，集成 Tools / MCP / Skills / Memory / Knowledge"""

from __future__ import annotations

from pathlib import Path

from agno.agent import Agent
from agno.skills import LocalSkills, Skills

from traveler.agents.prompts import TRAVEL_PLANNER_INSTRUCTIONS
from traveler.core.database import get_agent_db
from traveler.core.knowledge import get_travel_knowledge
from traveler.core.model_factory import create_model
from traveler.tools.travel_tools import TravelTools

# Skills 目录
SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def create_travel_planner(
    provider: str | None = None,
    model_id: str | None = None,
    user_id: str = "default",
    session_id: str | None = None,
    mcp_tools_list: list | None = None,
) -> Agent:
    """创建旅行规划主智能体

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        user_id: 用户 ID（用于 Memory 隔离）
        session_id: 会话 ID（用于 Session 持久化）
        mcp_tools_list: 已连接的 MCPTools 列表（由调用方管理生命周期）
    """
    model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()
    knowledge = get_travel_knowledge()

    # 构建工具列表
    tools: list = [TravelTools()]

    if mcp_tools_list:
        tools.extend(mcp_tools_list)

    # 加载 Skills
    skills = Skills(loaders=[LocalSkills(str(SKILLS_DIR))])

    agent = Agent(
        name="TravelPlanner",
        model=model,
        instructions=TRAVEL_PLANNER_INSTRUCTIONS,
        tools=tools,
        skills=skills,
        knowledge=knowledge,
        search_knowledge=True,
        db=db,
        update_memory_on_run=True,
        add_history_to_context=True,
        num_history_runs=5,
        session_state={"preferences": {}, "current_plan": {}},
        markdown=True,
    )

    return agent
