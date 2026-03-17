"""API 路由定义"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from loguru import logger

from traveler.api.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["travel"])

# 所有可用的 MCP 服务
ALL_MCP_SERVERS = ["google_maps", "web_search", "weather_search", "hotel_search"]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """与旅行规划智能体对话

    每次请求独立管理 MCP 连接的生命周期：connect → 使用 → close
    """
    from traveler.core.mcp_manager import MCPManager

    logger.info("收到请求: mode={} | user={}", request.mode, request.user_id)

    try:
        async with MCPManager(ALL_MCP_SERVERS) as mcp:
            mcp_tools = mcp.tools if mcp.tools else None

            match request.mode:
                case "agent":
                    from traveler.agents.travel_planner import create_travel_planner

                    agent = create_travel_planner(
                        provider=request.provider,
                        model_id=request.model_id,
                        user_id=request.user_id,
                        session_id=request.session_id,
                        mcp_tools=mcp_tools,
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
                        mcp_tools=mcp_tools,
                    )
                    response = await team.arun(request.message)
                    content = response.content if response.content else ""

                case "workflow":
                    from traveler.workflows.planning_workflow import create_planning_workflow

                    workflow = create_planning_workflow(
                        provider=request.provider,
                        model_id=request.model_id,
                        user_id=request.user_id,
                        session_id=request.session_id,
                        mcp_tools=mcp_tools,
                    )
                    response = await workflow.arun(request.message)
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
