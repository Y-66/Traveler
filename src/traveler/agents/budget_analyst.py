"""预算分析智能体 - 使用 TravelTools 估算费用并提供优化建议"""

from __future__ import annotations

from pathlib import Path

from agno.agent import Agent
from agno.skills import LocalSkills, Skills

from traveler.agents.prompts import BUDGET_ANALYST_INSTRUCTIONS
from traveler.core.database import get_agent_db
from traveler.core.model_factory import create_model
from traveler.tools.travel_tools import TravelTools

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def create_budget_analyst(
    provider: str | None = None,
    model_id: str | None = None,
) -> Agent:
    """创建预算分析智能体"""
    model = create_model(provider=provider, model_id=model_id)
    db = get_agent_db()

    skills = Skills(loaders=[LocalSkills(str(SKILLS_DIR / "budget-optimizer"))])

    return Agent(
        name="BudgetAnalyst",
        role="旅行预算分析师，使用工具估算费用并提供优化建议",
        model=model,
        instructions=BUDGET_ANALYST_INSTRUCTIONS,
        tools=[TravelTools()],
        skills=skills,
        db=db,
        markdown=True,
    )
