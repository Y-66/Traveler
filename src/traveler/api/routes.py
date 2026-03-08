"""API 路由定义"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from loguru import logger

from traveler.api.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["travel"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """与旅行规划智能体对话

    每次请求独立管理 MCP 连接的生命周期：connect → 使用 → close
    """
    from traveler.core.mcp_manager import MCPManager

    logger.info("收到请求: mode={} | user={}", request.mode, request.user_id)

    # 建立 MCP 连接
    mcp_manager = MCPManager()
    mcp_tools_list: list = []
    try:
        mcp_tools_list = await mcp_manager.connect()
    except Exception as e:
        logger.warning("MCP 连接失败，以离线模式处理: {}", e)

    try:
        match request.mode:
            case "agent":
                from traveler.agents.travel_planner import create_travel_planner

                agent = create_travel_planner(
                    provider=request.provider,
                    model_id=request.model_id,
                    user_id=request.user_id,
                    session_id=request.session_id,
                    mcp_tools_list=mcp_tools_list or None,
                )
                response = await agent.arun(request.message)
                content = response.content if response.content else ""

            case "team":
                from traveler.agents.team import create_travel_team

                team = create_travel_team(
                    provider=request.provider,
                    model_id=request.model_id,
                    user_id=request.user_id,
                    session_id=request.session_id,
                    mcp_tools_list=mcp_tools_list or None,
                )
                response = await team.arun(request.message)
                content = response.content if response.content else ""

            case "workflow":
                from traveler.workflows.planning_workflow import create_planning_workflow

                workflow = create_planning_workflow(
                    provider=request.provider,
                    model_id=request.model_id,
                    user_id=request.user_id,
                )
                response = workflow.run(request.message)
                content = response.content if response.content else ""

            case _:
                raise HTTPException(status_code=400, detail=f"不支持的模式: {request.mode}")

        return ChatResponse(
            content=content,
            session_id=request.session_id,
            metadata={"mode": request.mode},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("处理请求失败: {}", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 确保关闭 MCP 连接
        if mcp_manager.tools:
            await mcp_manager.close()
