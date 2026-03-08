import pytest
import pytest_asyncio

from traveler.core.mcp_manager import MCPManager

@pytest_asyncio.fixture
async def hotel_search_mcp():
    """
    提供酒店搜索 MCP 工具的异步 Fixture。
    使用 async with 确保测试完成后连接自动关闭。
    """
    async with MCPManager(["hotel_search"]) as manager:
        yield manager.get("hotel_search")

@pytest_asyncio.fixture
async def weather_mcp():
    """
    提供天气 MCP 工具的异步 Fixture。
    使用 async with 确保测试完成后连接自动关闭。
    """
    async with MCPManager(["weather"]) as manager:
        yield manager.get("weather")

@pytest_asyncio.fixture
async def google_route_mcp():
    """
    提供 Google Route MCP 工具的异步 Fixture。
    使用 async with 确保测试完成后连接自动关闭。
    """
    async with MCPManager(["google_route"]) as manager:
        yield manager.get("google_route")