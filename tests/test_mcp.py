import asyncio
from agno.agent import Agent
import pytest

from traveler.core.model_factory import create_model

@pytest.mark.asyncio
async def test_web_search_mcp(web_search_mcp):
    # 1. Arrange: 准备模型和 Agent
    model = create_model(provider="openai", model_id="gpt-4o")
    agent = Agent(
        model=model,
        name="Test Web Search Assistant",
        tools=[web_search_mcp],
        markdown=True
    )

    # 2. Act: 发起请求
    response = await agent.arun("帮我查找中国最新的新闻")

    # 3. Assert: 验证结果
    assert response is not None
    assert response.content is not None

    # 先断言它不是 None，Pylance 会自动推断后续代码中它一定是 List
    assert response.tools is not None

    # 验证 Agent 是否真的调用了工具（Agno 的 RunResponse 包含工具调用信息）
    # 这一步可以确保 Agent 没有在胡编乱造，而是真的去查了新闻
    assert len(response.tools) > 0
    search_functions = ['brave_web_search', 'brave_local_search', 'brave_video_search', 'brave_news_search', 'brave_image_search', 'brave_summarizer']
    assert any(tool.tool_name and tool.tool_name in search_functions for tool in response.tools)

@pytest.mark.asyncio
async def test_hotel_search_mcp(hotel_search_mcp):
    # 1. Arrange: 准备模型和 Agent
    model = create_model(provider="openai", model_id="gpt-4o")
    agent = Agent(
        model=model,
        name="Test Hotel Search Assistant",
        tools=[hotel_search_mcp],
        markdown=True
    )

    # 2. Act: 发起请求
    response = await agent.arun("帮我找一下在246 Main Street, Ottawa的酒店。")

    # 3. Assert: 验证结果
    assert response is not None
    assert response.content is not None

    # 先断言它不是 None，Pylance 会自动推断后续代码中它一定是 List
    assert response.tools is not None

    # 验证 Agent 是否真的调用了工具（Agno 的 RunResponse 包含工具调用信息）
    # 这一步可以确保 Agent 没有在胡编乱造，而是真的去查了酒店
    assert len(response.tools) > 0
    hotel_functions = ['airbnb_search', 'airbnb_listing_details']
    assert any(tool.tool_name and tool.tool_name in hotel_functions for tool in response.tools)

@pytest.mark.asyncio
async def test_weather_mcp(weather_search_mcp):
    # 1. Arrange: 准备模型和 Agent
    model = create_model(provider="openai", model_id="gpt-4o")
    agent = Agent(
        model=model,
        name="Test Weather Assistant",
        tools=[weather_search_mcp],
        markdown=True
    )

    # 2. Act: 发起请求
    # 使用 run() 而不是 print_response() 方便拿回结果进行断言
    response = await agent.arun("东京现在天气怎么样？")

    # 3. Assert: 验证结果
    # 验证响应不为空
    assert response is not None
    assert response.content is not None

    # 先断言它不是 None，Pylance 会自动推断后续代码中它一定是 List
    assert response.tools is not None
    
    # 验证 Agent 是否真的调用了工具（Agno 的 RunResponse 包含工具调用信息）
    # 这一步可以确保 Agent 没有在胡编乱造，而是真的去查了天气
    assert len(response.tools) > 0
    weather_functions = ['get_forecast', 'get_current_conditions', 'get_alerts']
    assert any(tool.tool_name and tool.tool_name in weather_functions for tool in response.tools)


@pytest.mark.asyncio
async def test_google_route_mcp(google_route_mcp):
    # 1. Arrange: 准备模型和 Agent
    model = create_model(provider="openai", model_id="gpt-4o")
    agent = Agent(
        model=model,
        name="Test Google Route Assistant",
        tools=[google_route_mcp],
        markdown=True
    )

    # 2. Act: 发起请求
    response = await agent.arun("从341 Main Street， Ottawa到123 Bank Street， Ottawa？")
    print("Agent Response:", response)

    # 3. Assert: 验证结果
    assert response is not None
    assert response.content is not None

    # 先断言它不是 None，Pylance 会自动推断后续代码中它一定是 List
    assert response.tools is not None

    # 验证 Agent 是否真的调用了工具（Agno 的 RunResponse 包含工具调用信息）
    # 这一步可以确保 Agent 没有在胡编乱造，而是真的去查了路线
    assert len(response.tools) > 0
    route_functions = ['search_places', 'lookup_weather', 'compute_routes']
    assert any(tool.tool_name and tool.tool_name in route_functions for tool in response.tools)

