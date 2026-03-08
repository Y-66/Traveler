from agno.tools.mcp import MCPTools
from mcp.client.stdio import StdioServerParameters, get_default_environment

def create_weather_search_mcp() -> MCPTools:
    """创建天气 MCP 服务工具。"""
    return MCPTools(
        server_params=StdioServerParameters(
            command="cmd",
            args=["/c", "npx", "-y", "@dangahagan/weather-mcp@latest"],
            env=get_default_environment(),
        )
    )
