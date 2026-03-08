"""预算分析智能体 - 专注于旅行费用估算与优化"""

from __future__ import annotations

from agno.agent import Agent

from traveler.agents.prompts import BUDGET_ANALYST_INSTRUCTIONS
from traveler.core.database import get_agent_db
from traveler.core.model_factory import create_model
from traveler.tools.travel_tools import TravelTools


def create_budget_analyst(
    provider: str | None = None,
    model_id: str | None = None,
) -> Agent:
    """创建预算分析智能体"""
    model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()

    return Agent(
        name="BudgetAnalyst",
        role="旅行预算分析师，负责费用估算和优化建议",
        model=model,
        instructions=BUDGET_ANALYST_INSTRUCTIONS,
        tools=[TravelTools()],
        db=db,
        markdown=True,
    )
