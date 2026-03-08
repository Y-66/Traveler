from traveler.core.mcp.hotel_search_mcp import create_hotel_search_mcp

from .google_route_mcp import create_google_route_mcp
from .weather_mcp import create_weather_mcp
from .web_search_mcp import create_search_mcp

# 映射服务名称到它们对应的工厂函数
AVAILABLE_MCPS = {
    "google_maps": create_google_route_mcp,
    "google_route": create_google_route_mcp, # 兼容老名称
    "weather": create_weather_mcp,
    "search": create_search_mcp,
    "hotel_search": create_hotel_search_mcp,
}

__all__ = ["AVAILABLE_MCPS"]
