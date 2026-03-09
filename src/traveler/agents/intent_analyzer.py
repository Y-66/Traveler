"""意图分析智能体 - 从自然语言中提取结构化旅行需求"""

from __future__ import annotations

from pathlib import Path

from agno.agent import Agent
from agno.skills import LocalSkills, Skills

from traveler.agents.prompts import INTENT_ANALYZER_INSTRUCTIONS
from traveler.core.model_factory import create_model

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def create_intent_analyzer(
    provider: str | None = None,
    model_id: str | None = None,
) -> Agent:
    """创建意图分析智能体"""
    model = create_model(provider=provider, model_id=model_id)
    skills = Skills(loaders=[LocalSkills(str(SKILLS_DIR / "intent-analysis"))])

    return Agent(
        name="IntentAnalyzer",
        role="旅行意图分析专家，从自然语言中提取结构化旅行需求",
        model=model,
        instructions=INTENT_ANALYZER_INSTRUCTIONS,
        skills=skills,
        markdown=False,  # 输出纯 JSON
    )
