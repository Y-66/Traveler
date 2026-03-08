"""旅游专用工具集 - 航班/酒店/景点搜索"""

from __future__ import annotations

from agno.tools import Toolkit
from loguru import logger


class TravelTools(Toolkit):
    """旅游数据查询工具集"""

    def __init__(self):
        super().__init__(name="travel_tools")
        self.register(self.search_flights)
        self.register(self.search_hotels)
        self.register(self.search_attractions)
        self.register(self.get_destination_info)
        self.register(self.estimate_budget)

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str = "",
        passengers: int = 1,
    ) -> str:
        """搜索航班信息

        Args:
            origin: 出发城市
            destination: 目的地城市
            departure_date: 出发日期 (YYYY-MM-DD)
            return_date: 返回日期 (YYYY-MM-DD)，留空表示单程
            passengers: 乘客人数
        """
        logger.info("搜索航班: {} -> {} | {}", origin, destination, departure_date)
        # TODO: 接入实际航班 API (如 Amadeus)
        return (
            f"找到 {origin} -> {destination} 的航班信息：\n"
            f"- 日期: {departure_date}\n"
            f"- 乘客: {passengers}人\n"
            f"- [示例] 航班 CA1234, 08:00-11:30, ¥1,280\n"
            f"- [示例] 航班 MU5678, 14:00-17:20, ¥980\n"
            f"注意: 当前为模拟数据，请接入实际 API 获取真实航班信息。"
        )

    def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str,
        guests: int = 2,
        budget_level: str = "medium",
    ) -> str:
        """搜索酒店信息

        Args:
            city: 目的地城市
            check_in: 入住日期 (YYYY-MM-DD)
            check_out: 离店日期 (YYYY-MM-DD)
            guests: 入住人数
            budget_level: 预算级别 (budget/medium/luxury)
        """
        logger.info("搜索酒店: {} | {} ~ {}", city, check_in, check_out)
        return (
            f"找到 {city} 的酒店信息：\n"
            f"- 入住: {check_in} ~ {check_out}\n"
            f"- 人数: {guests}人 | 预算: {budget_level}\n"
            f"- [示例] 城市花园酒店, ¥380/晚, 评分 4.5\n"
            f"- [示例] 海景度假酒店, ¥680/晚, 评分 4.8\n"
            f"注意: 当前为模拟数据，请接入实际 API 获取真实酒店信息。"
        )

    def search_attractions(self, city: str, category: str = "all") -> str:
        """搜索目的地景点信息

        Args:
            city: 目的地城市
            category: 景点类型 (all/nature/culture/entertainment/food)
        """
        logger.info("搜索景点: {} | 类别: {}", city, category)
        return (
            f"找到 {city} 的景点 (类别: {category})：\n"
            f"- [示例] 历史博物馆 - 文化类, 门票 ¥60, 建议游玩 2-3 小时\n"
            f"- [示例] 中央公园 - 自然类, 免费, 建议游玩 1-2 小时\n"
            f"- [示例] 美食街 - 美食类, 人均 ¥80\n"
            f"注意: 当前为模拟数据，请接入实际 API 获取真实景点信息。"
        )

    def get_destination_info(self, destination: str) -> str:
        """获取目的地综合信息（气候、签证、货币、时差等）

        Args:
            destination: 目的地名称
        """
        logger.info("获取目的地信息: {}", destination)
        return (
            f"{destination} 综合信息：\n"
            f"- 最佳旅游季节: 请根据具体目的地查询\n"
            f"- 当地货币: 请查询\n"
            f"- 签证要求: 请查询\n"
            f"- 安全提示: 请查询最新旅行建议\n"
            f"注意: 当前为模拟数据，请接入实际数据源。"
        )

    def estimate_budget(
        self,
        destination: str,
        days: int,
        travelers: int = 1,
        budget_level: str = "medium",
    ) -> str:
        """估算旅行预算

        Args:
            destination: 目的地
            days: 旅行天数
            travelers: 旅行人数
            budget_level: 预算级别 (budget/medium/luxury)
        """
        logger.info("估算预算: {} | {}天 | {}人", destination, days, travelers)

        daily_costs = {"budget": 300, "medium": 600, "luxury": 1500}
        daily = daily_costs.get(budget_level, 600)
        total = daily * days * travelers

        return (
            f"{destination} 旅行预算估算：\n"
            f"- 天数: {days}天 | 人数: {travelers}人\n"
            f"- 预算级别: {budget_level}\n"
            f"- 预估每人每天: ¥{daily}\n"
            f"- 预估总费用: ¥{total:,}\n"
            f"（含住宿、餐饮、交通、门票等基本开支）"
        )
