"""方案验证团队 - 多角色协作审查旅行方案"""

from __future__ import annotations

from agno.agent import Agent
from agno.team import Team
from agno.team.mode import TeamMode

from traveler.agents.prompts import (
    BUDGET_VALIDATOR_INSTRUCTIONS,
    LOGISTICS_VALIDATOR_INSTRUCTIONS,
    PRACTICALITY_VALIDATOR_INSTRUCTIONS,
    SCHEDULE_VALIDATOR_INSTRUCTIONS,
    VALIDATION_LEADER_INSTRUCTIONS,
)
from traveler.core.model_factory import create_model

def create_validation_team(
    provider: str | None = None,
    model_id: str | None = None,
) -> Team:
    """创建方案验证团队

    团队结构 (broadcast 模式):
        - Leader: 汇总各维度验证结论，输出最终 JSON
        - ScheduleValidator: 行程时间合理性
        - BudgetValidator: 预算数据一致性
        - LogisticsValidator: 路线逻辑与完整性
        - PracticalityValidator: 实际可行性

    broadcast 模式: 完整方案直接广播给所有成员，各自独立验证，leader 汇总。
    """
    model = create_model(provider=provider, model_id=model_id)
    leader_model = create_model(provider=provider, model_id=model_id)

    schedule_validator = Agent(
        name="ScheduleValidator",
        role="行程时间验证专家",
        model=model,
        instructions=SCHEDULE_VALIDATOR_INSTRUCTIONS,
        markdown=True,
    )

    budget_validator = Agent(
        name="BudgetValidator",
        role="预算验证专家",
        model=model,
        instructions=BUDGET_VALIDATOR_INSTRUCTIONS,
        markdown=True,
    )

    logistics_validator = Agent(
        name="LogisticsValidator",
        role="路线物流验证专家",
        model=model,
        instructions=LOGISTICS_VALIDATOR_INSTRUCTIONS,
        markdown=True,
    )

    practicality_validator = Agent(
        name="PracticalityValidator",
        role="实用性验证专家",
        model=model,
        instructions=PRACTICALITY_VALIDATOR_INSTRUCTIONS,
        markdown=True,
    )

    return Team(
        name="ValidationTeam",
        mode=TeamMode.broadcast,
        model=leader_model,
        members=[
            schedule_validator,
            budget_validator,
            logistics_validator,
            practicality_validator,
        ],
        instructions=VALIDATION_LEADER_INSTRUCTIONS,
        share_member_interactions=True,
        markdown=False,  # Leader 输出纯 JSON
    )


# 向后兼容别名
create_validator = create_validation_team
