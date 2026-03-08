import asyncio

from agno.agent import Agent

from traveler.core.model_factory import create_model
from traveler.core.mcp_manager import MCPManager
from mcp.client.session import ClientSession

# Google MCP 不支持 ping，禁用 ping
async def _noop_ping(self):
    return None

ClientSession.send_ping = _noop_ping # type: ignore

async def main():

    async with MCPManager(
        server_names=["google_maps", "hotel_search", "web_search"]
        ) as mcp:

        maps_tools = mcp.get("google_maps")
        hotel_mcp = mcp.get("hotel_search")
        web_search_mcp = mcp.get("web_search")

        if maps_tools is None:
            raise RuntimeError("google_maps MCP 未连接")
        
        if hotel_mcp is None:
            raise RuntimeError("hotel_search MCP 未连接")

        if web_search_mcp is None:
            raise RuntimeError("web_search MCP 未连接")

        print("可用工具:", list(web_search_mcp.functions.keys()))

        model = create_model(provider="openai", model_id="gpt-4o")

        agent = Agent(
            model=model,
            tools=[web_search_mcp],
            markdown=True
        )

        await agent.aprint_response(
            #"从 341 Main Street, Ottawa 到 123 Bank Street, Ottawa 怎么走？"
            #"帮我找一下在246 Main Street, Ottawa的酒店。"
            "帮我查找中国最新的新闻"
        )


if __name__ == "__main__":
    asyncio.run(main())