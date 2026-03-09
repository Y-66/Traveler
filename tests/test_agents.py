"""智能体创建测试 - 仅验证实例化，不实际调用 LLM"""

from traveler.agents.travel_planner import create_travel_planner
from traveler.agents.researcher import create_researcher
from traveler.agents.route_planner import create_route_planner
from traveler.agents.accommodation_advisor import create_accommodation_advisor
from traveler.agents.budget_analyst import create_budget_analyst
from traveler.agents.team import create_travel_team


def test_create_travel_planner():
    """测试旅行规划智能体可以正确创建（无 MCP）"""
    agent = create_travel_planner(mcp_tools=None)
    assert agent.name == "TravelPlanner"
    assert agent.markdown is True


def test_create_researcher():
    """测试研究智能体可以正确创建"""
    agent = create_researcher()
    assert agent.name == "TravelResearcher"
    assert agent.markdown is True


def test_create_route_planner():
    """测试路线规划智能体可以正确创建"""
    agent = create_route_planner()
    assert agent.name == "RoutePlanner"
    assert agent.markdown is True


def test_create_accommodation_advisor():
    """测试住宿顾问智能体可以正确创建"""
    agent = create_accommodation_advisor()
    assert agent.name == "AccommodationAdvisor"
    assert agent.markdown is True


def test_create_budget_analyst():
    """测试预算分析智能体可以正确创建"""
    agent = create_budget_analyst()
    assert agent.name == "BudgetAnalyst"
    assert agent.markdown is True


def test_create_travel_team():
    """测试旅行团队可以正确创建"""
    team = create_travel_team(mcp_tools=None)
    assert team.name == "TravelTeam"
    assert len(team.members) == 4
