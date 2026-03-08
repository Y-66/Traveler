"""API 请求/响应 Schema 定义"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """聊天请求"""

    message: str = Field(..., description="用户消息")
    user_id: str = Field(default="default", description="用户 ID")
    session_id: str | None = Field(default=None, description="会话 ID")
    mode: str = Field(default="agent", description="运行模式: agent / team / workflow")
    provider: str | None = Field(default=None, description="模型提供商")
    model_id: str | None = Field(default=None, description="模型 ID")


class ChatResponse(BaseModel):
    """聊天响应"""

    content: str = Field(..., description="智能体回复内容")
    session_id: str | None = Field(default=None, description="会话 ID")
    metadata: dict = Field(default_factory=dict, description="附加元数据")
