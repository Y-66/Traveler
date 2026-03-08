"""MCP 生命周期管理。"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from loguru import logger

from traveler.core.mcp import AVAILABLE_MCPS

class MCPManager:
    """简单管理一组 MCPTools 连接与关闭的上下文管理器。"""

    def __init__(self, server_names: Sequence[str]):
        """
        初始化 MCPManager。
        
        Args:
            server_names: 需要连接的 MCP 服务名称列表，例如 ["google_maps", "weather"]
        """
        self.server_names = server_names
        self.tools: dict[str, Any] = {}

    def get(self, name: str) -> Any | None:
        """获取已连接的 MCPTools 对象。"""
        return self.tools.get(name)

    async def __aenter__(self) -> MCPManager:
        """进入上下文，自动创建并连接所有指定的服务。"""
        for name in self.server_names:
            if name not in AVAILABLE_MCPS:
                logger.warning(f"未知的 MCP 服务: {name}。请在 core/mcp/__init__.py 中注册。")
                continue
                
            try:
                logger.info(f"正在连接 MCP 服务: {name}")
                # 从注册表中取出对应的工厂函数，并实例化 MCPTools
                tool = AVAILABLE_MCPS[name]()
                await tool.connect()
                logger.info(f"MCP 服务已连接: {name} ({len(tool.functions)} 个工具)")
                self.tools[name] = tool
            except Exception as e:
                logger.error(f"连接 MCP 服务 {name} 失败: {e}")
                
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文时自动关闭全部连接。"""
        for name, tool in list(self.tools.items()):
            try:
                await tool.close()
                logger.info(f"MCP 服务已关闭: {name}")
            except Exception as e:
                logger.error(f"关闭 MCP 服务 {name} 时发生错误: {e}")
        self.tools.clear()
