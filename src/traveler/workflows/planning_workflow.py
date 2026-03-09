"""旅行规划工作流 - 结构化的多步骤规划流程"""

from __future__ import annotations

from agno.workflow import Workflow

from traveler.agents.budget_analyst import create_budget_analyst
from traveler.agents.researcher import create_researcher
from traveler.agents.travel_planner import create_travel_planner
from traveler.core.database import get_agent_db


def create_planning_workflow(
    provider: str | None = None,
    model_id: str | None = None,
    user_id: str = "default",
) -> Workflow:
    """创建旅行规划工作流

    流程步骤:
        1. 研究员 → 收集目的地信息
        2. 预算师 → 估算和优化预算
        3. 规划师 → 生成完整行程

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        user_id: 用户 ID
    """
    db = get_agent_db()

    researcher = create_researcher(provider=provider, model_id=model_id)
    budget_analyst = create_budget_analyst(provider=provider, model_id=model_id)
    planner = create_travel_planner(
        provider=provider,
        model_id=model_id,
        user_id=user_id,
    )

    workflow = Workflow(
        name="TravelPlanningWorkflow",
        steps=[researcher, budget_analyst, planner],
        db=db,
    )

    return workflow
