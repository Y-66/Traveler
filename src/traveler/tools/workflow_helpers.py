"""工作流辅助函数 - 工作流步骤间的数据解析、格式化与上下文构建"""

from __future__ import annotations

import json

from loguru import logger

from agno.workflow import StepOutput
from agno.workflow.types import StepInput


# ---------------------------------------------------------------------------
# JSON 解析工具
# ---------------------------------------------------------------------------

def clean_json(raw: str) -> str:
    """清理可能包含 markdown 代码块标记的 JSON 字符串"""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()
    if cleaned.startswith("json"):
        cleaned = cleaned[4:].strip()
    return cleaned


def safe_parse_intent(raw: str, fallback_message: str = "") -> dict:
    """安全解析意图 JSON，失败时返回默认值"""
    try:
        return json.loads(clean_json(raw))
    except (json.JSONDecodeError, IndexError):
        return {
            "summary": fallback_message or raw,
            "destination": "未指定",
            "days": 5,
            "travelers": 1,
            "budget_level": "medium",
        }


# ---------------------------------------------------------------------------
# 上下文构建工具
# ---------------------------------------------------------------------------

def build_travel_context(intent: dict) -> str:
    """根据意图数据构建统一的旅行需求上下文"""
    destination = intent.get("destination", "未指定")
    origin = intent.get("origin", "")
    days = intent.get("days", 5)
    travelers = intent.get("travelers", 1)
    budget_level = intent.get("budget_level", "medium")
    budget_amount = intent.get("budget_amount")
    interests = intent.get("interests", [])
    special = intent.get("special_requirements")
    summary = intent.get("summary", "")

    lines = [
        "以下是用户的旅行需求，请根据你的专业角色完成相关分析：\n",
        f"- 目的地：{destination}",
        f"- 出发地：{origin or '未指定'}",
        f"- 天数：{days} 天",
        f"- 人数：{travelers} 人",
        f"- 预算级别：{budget_level}",
    ]
    if budget_amount:
        lines.append(f"- 预算金额：{budget_amount}")
    lines.append(f"- 兴趣偏好：{', '.join(interests) if interests else '无特殊偏好'}")
    if special:
        lines.append(f"- 特殊要求：{special}")
    if summary:
        lines.append(f"- 需求摘要：{summary}")

    return "\n".join(lines)


def extract_intent_from_parse(step_input: StepInput) -> dict:
    """从 parse_intent 步骤的输出中提取 intent JSON"""
    content = str(step_input.get_step_content("parse_intent") or "")
    marker = "<!-- INTENT_JSON:"
    end_marker = " -->"
    if marker in content:
        start = content.index(marker) + len(marker)
        end = content.index(end_marker, start)
        try:
            return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass
    return {}


# ---------------------------------------------------------------------------
# 工作流函数步骤（executor）
# ---------------------------------------------------------------------------

def parse_intent(step_input: StepInput) -> StepOutput:
    """解析意图分析的 JSON 输出，生成统一的旅行需求上下文供后续步骤使用。"""
    intent_raw = step_input.previous_step_content or ""
    original_input = step_input.input if isinstance(step_input.input, str) else ""

    logger.info("[parse_intent] 解析意图分析结果")

    intent = safe_parse_intent(intent_raw, original_input)
    destination = intent.get("destination", "未指定")
    days = intent.get("days", 5)
    travelers = intent.get("travelers", 1)
    budget_level = intent.get("budget_level", "medium")
    logger.info(f"[parse_intent] 目的地={destination}, {days}天, {travelers}人, 预算={budget_level}")

    context = build_travel_context(intent)

    content = (
        f"<!-- INTENT_JSON:{json.dumps(intent, ensure_ascii=False)} -->\n\n"
        f"{context}\n\n"
        f"请根据以上信息，发挥你的专业能力完成分析。"
    )

    return StepOutput(content=content)


def prepare_route(step_input: StepInput) -> StepOutput:
    """为路线规划智能体准备输入 — 结合意图上下文与研究结果"""
    logger.info("[prepare_route] 准备路线规划输入")

    intent = extract_intent_from_parse(step_input)
    research = str(step_input.get_step_content("destination_research") or "")
    context = build_travel_context(intent)

    content = (
        f"{context}\n\n"
        f"## 参考：目的地研究报告\n{research[:1500]}\n\n"
        f"请根据以上信息，规划详细的交通路线方案。"
    )

    return StepOutput(content=content)


def prepare_planning(step_input: StepInput) -> StepOutput:
    """汇总意图 + 研究结果，生成规划上下文供 accommodation 使用"""
    logger.info("[prepare_planning] 汇总研究结果 → 规划步骤输入")

    intent = extract_intent_from_parse(step_input)
    research = str(step_input.get_step_content("destination_research") or "暂无研究数据")
    route = str(step_input.get_step_content("route_research") or "暂无路线数据")
    context = build_travel_context(intent)

    content = (
        f"{context}\n\n"
        f"## 目的地研究报告摘要\n{research[:2000]}\n\n"
        f"## 路线规划报告摘要\n{route[:2000]}\n\n"
        f"请根据以上旅行需求和研究结果，发挥你的专业能力完成分析。"
    )

    return StepOutput(content=content)


def prepare_budget(step_input: StepInput) -> StepOutput:
    """为预算分析智能体准备输入 — 结合所有前序步骤信息"""
    logger.info("[prepare_budget] 准备预算分析输入")

    intent = extract_intent_from_parse(step_input)
    research = str(step_input.get_step_content("destination_research") or "")
    route = str(step_input.get_step_content("route_research") or "")
    accommodation = str(step_input.get_step_content("accommodation_planning") or "")
    context = build_travel_context(intent)

    content = (
        f"{context}\n\n"
        f"## 参考：目的地研究\n{research[:1000]}\n\n"
        f"## 参考：路线规划\n{route[:1000]}\n\n"
        f"## 参考：住宿推荐\n{accommodation[:1000]}\n\n"
        f"请根据以上信息，进行详细的预算分析。"
    )

    return StepOutput(content=content)


def prepare_validation(step_input: StepInput) -> StepOutput:
    """汇总所有步骤结果，格式化为验证步骤的输入"""
    logger.info("[prepare_validation] 汇总所有步骤结果")

    intent = extract_intent_from_parse(step_input)
    research = str(step_input.get_step_content("destination_research") or "")
    route = str(step_input.get_step_content("route_research") or "")
    accommodation = str(step_input.get_step_content("accommodation_planning") or "")
    budget = str(step_input.get_step_content("budget_planning") or "")

    content = (
        f"请验证以下旅行方案的完整性和合理性：\n\n"
        f"## 用户需求\n{json.dumps(intent, ensure_ascii=False, indent=2)}\n\n"
        f"## 目的地研究\n{research[:2000]}\n\n"
        f"## 路线规划\n{route[:2000]}\n\n"
        f"## 住宿推荐\n{accommodation[:2000]}\n\n"
        f"## 预算分析\n{budget[:2000]}\n\n"
        f"请根据你的专业角色，直接基于以上方案内容进行审查，输出发现的问题和建议。"
    )

    return StepOutput(content=content)


def prepare_report(step_input: StepInput) -> StepOutput:
    """汇总所有数据，格式化为报告生成步骤的输入"""
    logger.info("[prepare_report] 汇总所有数据生成报告输入")

    intent = extract_intent_from_parse(step_input)
    research = str(step_input.get_step_content("destination_research") or "")
    route = str(step_input.get_step_content("route_research") or "")
    accommodation = str(step_input.get_step_content("accommodation_planning") or "")
    budget = str(step_input.get_step_content("budget_planning") or "")
    validation = str(step_input.get_step_content("validation") or "")

    content = (
        f"请根据以下所有信息，生成一份完整的旅行报告：\n\n"
        f"## 用户需求\n{json.dumps(intent, ensure_ascii=False, indent=2)}\n\n"
        f"## 目的地研究报告\n{research}\n\n"
        f"## 路线规划报告\n{route}\n\n"
        f"## 住宿推荐报告\n{accommodation}\n\n"
        f"## 预算分析报告\n{budget}\n\n"
        f"## 方案验证结果\n{validation}\n\n"
        f"请整合以上所有信息，按照报告模板生成一份结构清晰、内容完整的旅行报告。"
        f"如果验证结果中有问题或建议，请在报告中进行修正和说明。"
    )

    return StepOutput(content=content)
