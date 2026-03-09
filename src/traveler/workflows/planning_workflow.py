"""
旅行规划工作流 - 企业级多步骤智能规划流程

工作流步骤:
    1.  Intent Analysis    — 解析用户自然语言，提取结构化旅行需求
    2.  Parse Intent       — 解析 JSON 并生成统一旅行上下文
    3.  Destination Research — 目的地深度研究（web_search + weather MCP）
    4.  Prepare Route      — 为路线规划准备上下文
    5.  Route Research     — 路线规划（google_maps MCP）
    6.  Prepare Planning   — 汇总研究结果，生成规划上下文
    7.  Accommodation      — 住宿推荐（hotel_search MCP）
    8.  Prepare Budget     — 为预算分析准备上下文
    9.  Budget Analysis    — 预算分析（TravelTools）
    10. Prepare Validation — 汇总所有结果，生成验证输入
    11. Validation         — 验证团队审查方案合理性
    12. Prepare Report     — 汇总所有数据，生成报告输入
    13. Report Generation  — 生成最终旅行报告
"""

from __future__ import annotations

from typing import Any

from agno.workflow import Step, Workflow
from agno.memory.manager import MemoryManager

from traveler.agents.accommodation_advisor import create_accommodation_advisor
from traveler.agents.budget_analyst import create_budget_analyst
from traveler.agents.intent_analyzer import create_intent_analyzer
from traveler.agents.report_generator import create_report_generator
from traveler.agents.researcher import create_researcher
from traveler.agents.route_planner import create_route_planner
from traveler.agents.validator import create_validation_team

from traveler.core.database import get_memory_db, get_workflow_db
from traveler.core.model_factory import create_model

from traveler.tools.workflow_helpers import (
    parse_intent,
    prepare_budget,
    prepare_planning,
    prepare_report,
    prepare_route,
    prepare_validation,
)


# ---------------------------------------------------------------------------
# 工作流工厂
# ---------------------------------------------------------------------------

def create_planning_workflow(
    provider: str | None = None,
    model_id: str | None = None,
    user_id: str = "default",
    session_id: str | None = None,
    mcp_tools: dict[str, Any] | None = None,
) -> Workflow:
    """创建旅行规划工作流

    流程（顺序执行，避免并发 MCP 会话冲突）:
        1.  IntentAnalyzer        → 解析用户需求
        2.  parse_intent          → 解析 JSON + 生成统一上下文
        3.  destination_research  → 目的地深度研究
        4.  prepare_route         → 为路线规划准备上下文
        5.  route_research        → 路线规划
        6.  prepare_planning      → 汇总 → 住宿规划上下文
        7.  accommodation         → 住宿推荐
        8.  prepare_budget        → 汇总 → 预算分析上下文
        9.  budget_planning       → 预算分析
        10. prepare_validation    → 汇总 → 验证输入
        11. validation            → 方案验证
        12. prepare_report        → 汇总 → 报告输入
        13. report                → 生成最终报告

    Args:
        provider: 模型提供商
        model_id: 模型 ID
        user_id: 用户 ID
        session_id: 会话 ID
        mcp_tools: MCP 工具字典 (来自 MCPManager.tools)
    """
    db = get_workflow_db()
    memory_db = get_memory_db()

    # --- 创建各智能体 ---
    intent_analyzer = create_intent_analyzer(provider=provider, model_id=model_id)

    researcher = create_researcher(
        provider=provider, model_id=model_id, mcp_tools=mcp_tools,
    )
    route_planner = create_route_planner(
        provider=provider, model_id=model_id, mcp_tools=mcp_tools,
    )
    accommodation = create_accommodation_advisor(
        provider=provider, model_id=model_id, mcp_tools=mcp_tools,
    )
    budget_analyst = create_budget_analyst(provider=provider, model_id=model_id)

    validator = create_validation_team(provider=provider, model_id=model_id)

    report_generator = create_report_generator(provider=provider, model_id=model_id)
    # 为报告生成器启用 memory，记住用户偏好
    memory_model = create_model(provider=provider, model_id=model_id)
    report_generator.memory_manager = MemoryManager(
        model=memory_model,
        db=memory_db,
    )
    report_generator.update_memory_on_run = True

    # --- 构建工作流（顺序执行，MCP 会话安全）---
    steps = [
        # Step 1: 意图分析 (Agent)
        Step(name="intent_analysis", agent=intent_analyzer),
        # Step 2: 解析意图 + 生成统一上下文 (Function)
        Step(name="parse_intent", executor=parse_intent),
        # Step 3: 目的地研究 (Agent + web_search / weather MCP)
        Step(name="destination_research", agent=researcher),
        # Step 4: 准备路线规划上下文 (Function)
        Step(name="prepare_route", executor=prepare_route),
        # Step 5: 路线规划 (Agent + google_maps MCP)
        Step(name="route_research", agent=route_planner),
        # Step 6: 汇总研究 → 住宿规划上下文 (Function)
        Step(name="prepare_planning", executor=prepare_planning),
        # Step 7: 住宿推荐 (Agent + hotel_search MCP)
        Step(name="accommodation_planning", agent=accommodation),
        # Step 8: 准备预算分析上下文 (Function)
        Step(name="prepare_budget", executor=prepare_budget),
        # Step 9: 预算分析 (Agent + TravelTools)
        Step(name="budget_planning", agent=budget_analyst),
        # Step 10: 汇总 → 验证输入 (Function)
        Step(name="prepare_validation", executor=prepare_validation),
        # Step 11: 方案验证 (Team: 多角色协作审查)
        Step(name="validation", team=validator),
        # Step 12: 汇总 → 报告输入 (Function)
        Step(name="prepare_report", executor=prepare_report),
        # Step 13: 生成最终报告 (Agent)
        Step(name="report", agent=report_generator),
    ]

    workflow = Workflow(
        name="TravelPlanningWorkflow",
        description="企业级旅行规划工作流：意图分析 → 研究 → 路线 → 住宿 → 预算 → 验证 → 报告",
        steps=steps,
        db=db,
        user_id=user_id,
        session_id=session_id,
        store_events=True,
    )

    return workflow