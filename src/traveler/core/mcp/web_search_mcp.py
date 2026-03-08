from agno.tools.mcp import MCPTools
from mcp.client.stdio import StdioServerParameters, get_default_environment
from traveler.config.settings import get_settings

def create_web_search_mcp() -> MCPTools:
    """创建网页搜索 (Brave Search) MCP 服务工具。"""
    settings = get_settings()
    env = {**get_default_environment()}
    if settings.brave_api_key:
        env["BRAVE_API_KEY"] = settings.brave_api_key
        
    return MCPTools(
        server_params=StdioServerParameters(
            command="cmd",
            args=["/c", "npx", "-y", "@brave/brave-search-mcp-server", "--transport", "stdio"],
            env=env,
        )
    )
