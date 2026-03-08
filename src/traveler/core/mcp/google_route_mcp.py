from agno.tools.mcp import MCPTools, StreamableHTTPClientParams
from traveler.config.settings import get_settings
import os

def create_google_route_mcp() -> MCPTools:
    """创建 Google Maps MCP 服务工具。"""
    settings = get_settings()
    headers: dict[str, str] = {}
    
    # 支持 settings 里面的 google_api_key 或系统环境变量 X_GOOG_API_KEY
    api_key = settings.google_api_key or os.environ.get("X_GOOG_API_KEY")
    if api_key:
        headers["X-Goog-Api-Key"] = api_key
        
    return MCPTools(
        server_params=StreamableHTTPClientParams(
            url="https://mapstools.googleapis.com/mcp",
            headers=headers,
        ),
        transport="streamable-http",
    )

