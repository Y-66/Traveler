"""智能体创建测试 - 仅验证实例化，不实际调用 LLM"""

from traveler.agents.travel_planner import create_travel_planner


def test_create_travel_planner():
    """测试旅行规划智能体可以正确创建（无 MCP）"""
    agent = create_travel_planner(mcp_tools_list=None)
    assert agent.name == "TravelPlanner"
    assert agent.markdown is True
