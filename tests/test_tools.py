"""工具模块单元测试"""

from traveler.tools.travel_tools import TravelTools


def test_travel_tools_search_flights():
    """测试航班搜索工具"""
    tools = TravelTools()
    result = tools.search_flights(
        origin="北京",
        destination="上海",
        departure_date="2026-04-01",
    )
    assert "北京" in result
    assert "上海" in result


def test_travel_tools_search_hotels():
    """测试酒店搜索工具"""
    tools = TravelTools()
    result = tools.search_hotels(
        city="上海",
        check_in="2026-04-01",
        check_out="2026-04-03",
    )
    assert "上海" in result


def test_travel_tools_estimate_budget():
    """测试预算估算工具"""
    tools = TravelTools()
    result = tools.estimate_budget(
        destination="东京",
        days=5,
        travelers=2,
        budget_level="medium",
    )
    assert "东京" in result
    assert "6,000" in result  # 600 * 5 * 2 = 6000
