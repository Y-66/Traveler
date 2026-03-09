"""报告生成智能体 - 整合各步骤输出生成完整旅行报告"""

from __future__ import annotations

from pathlib import Path

from agno.agent import Agent
from agno.skills import LocalSkills, Skills

from traveler.agents.prompts import REPORT_GENERATOR_INSTRUCTIONS
from traveler.core.model_factory import create_model

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def create_report_generator(
    provider: str | None = None,
    model_id: str | None = None,
) -> Agent:
    """创建报告生成智能体"""
    model = create_model(provider=provider, model_id=model_id)
    skills = Skills(loaders=[LocalSkills(str(SKILLS_DIR / "report-generation"))])

    return Agent(
        name="ReportGenerator",
        role="旅行报告生成专家，将各步骤产出整合为完整的旅行报告",
        model=model,
        instructions=REPORT_GENERATOR_INSTRUCTIONS,
        skills=skills,
        markdown=True,
    )
