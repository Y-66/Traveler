"""旅行规划团队 - 4 角色协作模式"""

from __future__ import annotations

from typing import Any

from agno.team import Team
from agno.team.mode import TeamMode

from traveler.agents.accommodation_advisor import create_accommodation_advisor
from traveler.agents.budget_analyst import create_budget_analyst
from traveler.agents.prompts import TEAM_LEADER_INSTRUCTIONS
from traveler.agents.researcher import create_researcher
from traveler.agents.route_planner import create_route_planner
from traveler.core.database import get_agent_db
from traveler.core.model_factory import create_model


def create_travel_team(
    provider: str | None = None,
    model_id: str | None = None,
    user_id: str = "default",
    session_id: str | None = None,
    mcp_tools: dict[str, Any] | None = None,
) -> Team:
    """创建旅行规划团队

    团队结构:
        - Leader: 协调全局（coordinate 模式）
        - TravelResearcher: 目的地研究（web_search + weather MCP）
        - RoutePlanner: 路线规划（google_maps MCP）
        - AccommodationAdvisor: 住宿推荐（hotel_search MCP）
        - BudgetAnalyst: 预算分析（TravelTools）

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        user_id: 用户 ID
        session_id: 会话 ID
        mcp_tools: MCP 工具字典 {"google_maps": tool, "web_search": tool, ...}
    """
    leader_model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()

    # 各角色分配对应的 MCP 工具
    researcher = create_researcher(
        provider=provider, model_id=model_id, mcp_tools=mcp_tools
    )
    route_planner = create_route_planner(
        provider=provider, model_id=model_id, mcp_tools=mcp_tools
    )
    accommodation = create_accommodation_advisor(
        provider=provider, model_id=model_id, mcp_tools=mcp_tools
    )
    budget_analyst = create_budget_analyst(
        provider=provider, model_id=model_id
    )

    team = Team(
        name="TravelTeam",
        mode=TeamMode.coordinate,
        model=leader_model,
        members=[researcher, route_planner, accommodation, budget_analyst],
        instructions=TEAM_LEADER_INSTRUCTIONS,
        db=db,
        markdown=True,
    )

    return team
