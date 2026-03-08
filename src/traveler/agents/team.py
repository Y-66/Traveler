"""旅行规划团队 - 多智能体协作模式"""

from __future__ import annotations

from agno.team import Team, TeamMode

from traveler.agents.budget_analyst import create_budget_analyst
from traveler.agents.researcher import create_researcher
from traveler.agents.travel_planner import create_travel_planner
from traveler.core.database import get_agent_db
from traveler.core.model_factory import create_model


def create_travel_team(
    provider: str | None = None,
    model_id: str | None = None,
    user_id: str = "default",
    session_id: str | None = None,
    mcp_tools_list: list | None = None,
) -> Team:
    """创建旅行规划团队

    团队结构:
        - Leader: 旅行规划师（协调全局）
        - Member: 旅行研究员（使用 MCP 搜集信息）
        - Member: 预算分析师（费用优化）

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        user_id: 用户 ID
        session_id: 会话 ID
        mcp_tools_list: 已连接的 MCPTools 列表（由调用方管理生命周期）
    """
    leader_model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()

    # MCP 工具交给研究员使用
    researcher = create_researcher(
        provider=provider, model_id=model_id, mcp_tools_list=mcp_tools_list
    )
    budget_analyst = create_budget_analyst(provider=provider, model_id=model_id)
    planner = create_travel_planner(
        provider=provider,
        model_id=model_id,
        user_id=user_id,
        session_id=session_id,
        mcp_tools_list=None,  # MCP 由 researcher 负责
    )

    team = Team(
        name="TravelTeam",
        mode=TeamMode.coordinate,
        model=leader_model,
        members=[planner, researcher, budget_analyst],
        instructions=(
            "你是旅行规划团队的负责人。根据用户需求，协调团队成员完成旅行规划：\n"
            "1. 让 TravelResearcher 搜集目的地信息和实时数据\n"
            "2. 让 BudgetAnalyst 进行预算分析和优化\n"
            "3. 让 TravelPlanner 整合所有信息生成完整行程\n"
            "确保最终输出包含完整行程、预算明细和实用建议。"
        ),
        db=db,
        markdown=True,
    )

    return team
