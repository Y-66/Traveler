"""测试旅行规划团队的完整调用流程"""

import asyncio

from mcp.client.session import ClientSession

from traveler.agents.team import create_travel_team
from traveler.core.mcp_manager import MCPManager

# Google MCP 不支持 ping，禁用 ping
async def _noop_ping(self):
    return None

ClientSession.send_ping = _noop_ping  # type: ignore


async def main():
    # 连接所有 MCP 服务
    async with MCPManager(
        server_names=["google_maps", "hotel_search", "web_search", "weather_search"]
    ) as mcp:
        # 打印已连接的 MCP 服务
        for name, tool in mcp.tools.items():
            print(f"✅ {name}: {list(tool.functions.keys())}")

        # 创建旅行团队，将 MCP 工具字典传入
        team = create_travel_team(
            provider="openai",
            model_id="gpt-4o-mini",
            mcp_tools=mcp.tools,
        )

        # 发起旅行规划请求
        await team.aprint_response(
            "帮我规划一个从北京到东京的5天旅行，预算中等，2个人。",
            stream=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
