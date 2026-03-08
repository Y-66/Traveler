# 🌍 Traveler - 企业级旅游规划智能体

基于 [Agno](https://docs.agno.com) 框架构建的企业级旅游规划智能体系统。集成 MCP、Skills、Memory、Knowledge、Team 等能力，提供个性化的旅行规划服务。

## 🏗️ 项目架构

```
Traveler/
├── .env.example                # 环境变量模板
├── .gitignore                  # Git 忽略规则
├── .pre-commit-config.yaml     # Pre-commit 钩子配置
├── pyproject.toml              # 项目配置 (依赖 / 工具链)
├── README.md                   # 项目文档
│
├── src/traveler/               # 主源码目录
│   ├── __init__.py
│   ├── cli.py                  # CLI 入口 (typer)
│   │
│   ├── config/                 # 配置模块
│   │   ├── settings.py         # Pydantic Settings 配置
│   │   └── logging.py          # Loguru 日志配置
│   │
│   ├── core/                   # 核心模块
│   │   ├── model_factory.py    # LLM 模型工厂
│   │   ├── database.py         # 数据库初始化
│   │   └── knowledge.py        # 知识库管理
│   │
│   ├── agents/                 # 智能体定义
│   │   ├── prompts.py          # Prompt 模板
│   │   ├── travel_planner.py   # 旅行规划主智能体
│   │   ├── researcher.py       # 研究员智能体
│   │   ├── budget_analyst.py   # 预算分析师智能体
│   │   └── team.py             # 多智能体团队
│   │
│   ├── tools/                  # 工具模块
│   │   ├── travel_tools.py     # 旅游专用工具集 (Toolkit)
│   │   └── mcp_tools.py        # MCP 工具集成 (天气/搜索/地图)
│   │
│   ├── skills/                 # 智能体技能 (Agno Skills)
│   │   ├── travel-planning/    # 旅行规划技能
│   │   ├── local-expert/       # 本地专家技能
│   │   └── budget-optimizer/   # 预算优化技能
│   │
│   ├── workflows/              # 工作流
│   │   └── planning_workflow.py
│   │
│   ├── knowledge_docs/         # 知识库文档
│   │   └── README.md
│   │
│   └── api/                    # FastAPI 服务
│       ├── app.py              # 应用工厂
│       ├── routes.py           # 路由定义
│       └── schemas.py          # 请求/响应 Schema
│
├── tests/                      # 测试目录
│   ├── test_config.py
│   ├── test_tools.py
│   └── test_agents.py
│
└── data/                       # 运行时数据 (git ignored)
    ├── traveler.db             # SQLite 数据库
    └── chromadb/               # 向量数据库
```

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| **Agent** | 基于 Agno Agent 的旅行规划智能体，支持工具调用和多轮对话 |
| **Team** | 多智能体协作：规划师 + 研究员 + 预算师 |
| **Workflow** | 结构化工作流：研究 → 预算 → 规划 |
| **MCP** | 通过 MCP 接入天气、搜索、地图等外部服务 |
| **Skills** | 旅行规划、本地专家、预算优化等专业技能包 |
| **Memory** | 自动记忆用户偏好和历史信息 |
| **Knowledge** | 向量数据库存储旅游知识文档，支持语义检索 |
| **Tools** | 自定义航班/酒店/景点搜索工具集 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 激活 conda 环境
conda activate agno

# 安装依赖
pip install -e ".[dev]"
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env，填入你的 API Key
```

### 3. 运行

```bash
# 交互式对话 (单智能体模式)
traveler chat

# 团队协作模式
traveler chat --mode team

# 工作流模式
traveler chat --mode workflow

# 指定模型
traveler chat --provider anthropic --model-id claude-sonnet-4-20250514

# 禁用 MCP (离线模式)
traveler chat --no-mcp
```

### 4. API 服务

```bash
# 启动 API
traveler serve

# 开发模式 (热重载)
traveler serve --reload

# 调用 API
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "帮我规划一个5天的东京旅行", "mode": "agent"}'
```

### 5. 知识库

```bash
# 将文档放入 src/traveler/knowledge_docs/ 目录
# 然后加载到向量数据库
traveler load-knowledge
```

## 🧪 测试

```bash
pytest
pytest --cov=traveler
```

## 📦 技术栈

- **Agno** - 智能体框架 (Agent / Team / Workflow / MCP / Skills)
- **FastAPI** - Web API 框架
- **Pydantic** - 数据验证
- **ChromaDB** - 向量数据库
- **SQLite** - 会话与记忆存储 (生产环境可切换 PostgreSQL)
- **Loguru** - 日志系统
- **Typer** - CLI 框架
- **Rich** - 终端美化

## 📄 License

MIT
