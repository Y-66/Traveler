from agno.tools.mcp import MCPTools
from mcp.client.stdio import StdioServerParameters, get_default_environment

def create_hotel_search_mcp() -> MCPTools:
    """创建酒店搜索 MCP 服务工具。"""
    return MCPTools(
        server_params=StdioServerParameters(
            command="cmd",
            args=["/c", "npx", "-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
            env=get_default_environment(),
        )
    )
