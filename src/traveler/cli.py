"""Traveler CLI - 命令行入口"""

from __future__ import annotations

import asyncio

import typer
from rich.console import Console
from rich.panel import Panel

from traveler.config.logging import setup_logging

app = typer.Typer(
    name="traveler",
    help="🌍 Traveler - 企业级旅游规划智能体",
    no_args_is_help=True,
)
console = Console()


# ---------------------------------------------------------------------------
# 异步对话核心
# ---------------------------------------------------------------------------


async def _run_chat(
    mode: str,
    provider: str | None,
    model_id: str | None,
    user_id: str,
    no_mcp: bool,
) -> None:
    """异步对话主循环，管理 MCP 连接的完整生命周期"""
    from traveler.core.mcp_manager import MCPManager

    # 所有可用的 MCP 服务
    all_servers = ["google_maps", "web_search", "weather_search", "hotel_search"]

    if no_mcp:
        # 无 MCP 模式
        runner = _create_runner(mode, provider, model_id, user_id, mcp_tools=None)
        await _chat_loop(runner)
    else:
        async with MCPManager(all_servers) as mcp:
            console.print(f"[dim]MCP 已连接: {list(mcp.tools.keys())}[/dim]")
            runner = _create_runner(mode, provider, model_id, user_id, mcp_tools=mcp.tools)
            await _chat_loop(runner)


def _create_runner(mode, provider, model_id, user_id, mcp_tools):
    """根据模式创建对应的智能体/团队"""
    match mode:
        case "agent":
            from traveler.agents.travel_planner import create_travel_planner
            return create_travel_planner(
                provider=provider,
                model_id=model_id,
                user_id=user_id,
                mcp_tools=mcp_tools,
            )
        case "team":
            from traveler.agents.team import create_travel_team
            return create_travel_team(
                provider=provider,
                model_id=model_id,
                user_id=user_id,
                mcp_tools=mcp_tools,
            )
        case "workflow":
            from traveler.workflows.planning_workflow import create_planning_workflow
            return create_planning_workflow(
                provider=provider,
                model_id=model_id,
                user_id=user_id,
                mcp_tools=mcp_tools,
            )
        case _:
            raise ValueError(f"不支持的模式: {mode}")


async def _chat_loop(runner) -> None:
    """交互式对话循环"""
    while True:
        try:
            user_input = console.input("\n[bold cyan]你: [/bold cyan]")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip().lower() in ("quit", "exit", "q"):
            console.print("[yellow]再见！祝旅途愉快！ 🛫[/yellow]")
            break

        if not user_input.strip():
            continue

        console.print()
        await runner.aprint_response(user_input, stream=True)


# ---------------------------------------------------------------------------
# CLI 命令
# ---------------------------------------------------------------------------


@app.command()
def chat(
    mode: str = typer.Option("agent", help="运行模式: agent / team / workflow"),
    provider: str = typer.Option(None, help="模型提供商: openai / anthropic / deepseek"),
    model_id: str = typer.Option(None, help="模型 ID"),
    user_id: str = typer.Option("default", help="用户 ID"),
    no_mcp: bool = typer.Option(False, help="禁用 MCP 工具"),
):
    """启动交互式旅行规划对话"""
    setup_logging()

    console.print(
        Panel.fit(
            "[bold green]🌍 Traveler 旅行规划助手[/bold green]\n"
            f"模式: {mode} | 提供商: {provider or '默认'}\n"
            "输入 'quit' 或 'exit' 退出",
            border_style="green",
        )
    )

    asyncio.run(_run_chat(mode, provider, model_id, user_id, no_mcp))


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="监听地址"),
    port: int = typer.Option(8000, help="监听端口"),
    reload: bool = typer.Option(False, help="开发模式热重载"),
):
    """启动 API 服务"""
    import uvicorn

    setup_logging()
    console.print(f"[green]🚀 启动 API 服务: http://{host}:{port}[/green]")
    uvicorn.run(
        "traveler.api.app:create_app",
        host=host,
        port=port,
        reload=reload,
        factory=True,
    )


@app.command()
def load_knowledge():
    """加载知识库文档到向量数据库"""
    setup_logging()
    from traveler.core.knowledge import load_knowledge_documents

    console.print("[cyan]正在加载知识库文档...[/cyan]")
    load_knowledge_documents()
    console.print("[green]✅ 知识库加载完成[/green]")


if __name__ == "__main__":
    app()
