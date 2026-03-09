"""
测试旅行规划工作流的完整调用流程

使用方法:
    1. 确保 .env 中配置了 OPENAI_API_KEY、BRAVE_API_KEY、GOOGLE_API_KEY
    2. 激活 conda 环境: conda activate agno
    3. 运行: python tests/workflow_call.py

工作流流程 (13 步顺序执行):
    意图分析 → 解析意图 → 目的地研究 → 路线规划 → 住宿推荐
    → 预算分析 → 方案验证 → 报告生成
"""

import asyncio

from loguru import logger
from mcp.client.session import ClientSession

from traveler.core.mcp_manager import MCPManager
from traveler.workflows.planning_workflow import create_planning_workflow

# Google Maps MCP 不支持 ping，需要禁用
_original_send_ping = ClientSession.send_ping


async def _noop_ping(self):
    return None


ClientSession.send_ping = _noop_ping  # type: ignore


async def main():
    logger.info("=" * 60)
    logger.info("旅行规划工作流 - 启动")
    logger.info("=" * 60)

    # 连接所有 MCP 服务
    async with MCPManager(
        server_names=["google_maps", "hotel_search", "web_search", "weather_search"]
    ) as mcp:
        # 打印已连接的 MCP 服务
        for name, tool in mcp.tools.items():
            logger.info(f"MCP 已连接: {name} ({len(tool.functions)} 个工具)")

        # 创建工作流
        workflow = create_planning_workflow(
            provider="openai",
            model_id="gpt-4o-mini",
            mcp_tools=mcp.tools,
        )

        logger.info(f"工作流已创建: {workflow.name}")
        logger.info(f"步骤数: {len(workflow.steps)}")
        logger.info("-" * 60)

        # 执行工作流（在 MCP 上下文内 try/except，保证 MCP 会话不会提前关闭）
        try:
            await workflow.aprint_response(
                input="帮我规划一个从北京到东京的5天旅行，预算中等，2个人，喜欢美食和文化体验。",
                stream=True,
                markdown=True,
                show_step_details=True,
            )
        except Exception:
            logger.exception("工作流执行出错")

    logger.info("工作流执行完毕")


if __name__ == "__main__":
    asyncio.run(main())
