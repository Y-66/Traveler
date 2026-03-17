# 🌍 Traveler - Enterprise Travel Planning Agent System / 企业级旅游规划智能体

基于 [Agno](https://docs.agno.com) 框架构建的企业级旅游规划智能体系统。集成 MCP、Skills、Memory、Knowledge、Team 等能力，提供个性化的旅行规划服务。

## 🏗️ Architecture & Structure

```text
Traveler/
├── .env.example                # Environment variables template
├── pyproject.toml              # Project configuration and dependencies (Hatch build system)
├── data/                       # Local data storage (SQLite, ChromaDB outputs, reports)
├── src/traveler/               # Main source code directory
│   ├── agents/                 # Agent Definitions (Planner, Researcher, Budget Analyst, Team)
│   ├── api/                    # FastAPI web service (app, routes, schemas)
│   ├── config/                 # Pydantic Settings & Loguru configurations
│   ├── core/                   # Core Infrastructure (Model Factory, Database Setup, Knowledge Management)
│   │   └── mcp/                # External MCP Server Clients (Weather, Google Routes, etc.)
│   ├── knowledge_docs/         # Document drop-zone for RAG Knowledge base
│   ├── skills/                 # Pluggable Agno Skills (Budget, Intent, Local Expert, Validation)
│   ├── tools/                  # Custom callable tools and workflow helpers
│   ├── workflows/              # Agno Workflows (planning_workflow.py)
│   └── cli.py                  # Typer-based CLI Entry Point
└── tests/                      # Pytest suite
```

## 🚀 Quick Start

### 1. Environment Setup

Traveler requires **Python 3.12+**.

```bash
# Create and activate a Conda environment
conda create -n agno python=3.12
conda activate agno

# Install dependencies (including dev tools)
pip install -e ".[dev]"
```

### 2. Configuration

```bash
# Copy the environment file template
cp .env.example .env

# Edit .env and supply your LLM Provider and MCP API Keys
# Supported LLM providers: OpenAI, Anthropic, etc.
```

### 3. CLI Usage

The system includes a rich CLI powered by Typer.

```bash
# Interactive Chat (Single Agent Mode)
traveler chat

# Team Collaboration Mode (Planner + Researcher + Budget Analyst)
traveler chat --mode team

# Workflow Pipeline Mode (Structured steps: Research -> Budget -> Plan)
traveler chat --mode workflow

# Specify an LLM Provider and Model
traveler chat --provider anthropic --model-id claude-3-5-sonnet-20241022

# Offline / No-MCP Mode (Disables external MCP tools)
traveler chat --no-mcp
```

### 4. API Service

Traveler can run as a stateful FastAPI backend.

```bash
# Start the FastAPI server
traveler serve

# Development mode with hot-reloading
traveler serve --reload

# Usage example (cURL)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a 5-day trip to Tokyo", "mode": "agent"}'
```

### 5. Knowledge Management

To empower the agent with your own customized guides:
1. Place PDF/Markdown guides in `src/traveler/knowledge_docs/`
2. Run the load command to vectorize them into local ChromaDB:
```bash
traveler load-knowledge
```

## 📦 Tech Stack

- **[Agno](https://docs.agno.com)**: Core Agentic Framework (Agent, Team, Workflow, MCP, Skills)
- **FastAPI / Uvicorn / Pydantic**: Robust Web API & Data Validation
- **ChromaDB / LanceDB**: Vector Databases for Knowledge (RAG)
- **SQLite / SQLAlchemy**: Session Memory & Persistence Base (Easily swapped to Postgres)
- **Typer & Rich**: Powerful and beautiful CLI creation
- **Loguru**: Modern Python logging

## 📄 License

MIT License.

---

<br/>

<a id="中文版"></a>
# 中文版

**Traveler** 是一个基于 [Agno](https://docs.agno.com) 框架构建的企业级旅游规划智能体系统。通过深度集成 **MCP (Model Context Protocol)**、**Skills(技能)**、**Memory(记忆)**、**Knowledge(知识库)**、**Team(团队协作)** 以及 **Workflow(工作流)** 等能力，Traveler 为用户提供高度定制化、全面且信息实时的旅行规划服务。

**Result**: 
- **English**: [Report presentaion](./public/report_eng.md)

- **Chinese**: [报告展示](./public/report_zh.md)

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| **Agent (智能体)** | 基于 Agno 构建的旅行主规划师，支持复杂的工具调用、多轮对话状态保持与自主推理。 |
| **Team (多智能体协作)** | 协作模式：通过统筹 *规划师*、*研究员* 和 *预算分析师* 等多个专职 Agent，实现复杂的规划协作。 |
| **Workflow (工作流)** | 结构化的流水线执行：研究与信息搜集 → 预算分析 → 行程提炼与规划生成。 |
| **MCP (模型上下文协议)** | 原生集成外部 MCP 服务，可实时获取天气预报、网络搜索信息、酒店库存以及谷歌路线分析。 |
| **Skills (技能插件)** | 载入各个垂直领域的 Agno Skills，涵盖：*旅游规划*、*本地专家指南*、*意图分析*及*预算优化*。 |
| **Memory (记忆系统)** | 自动提取和持久化用户的偏好（饮食、住宿要求、预算上限等）及历史对话记录，实现个性化服务。 |
| **Knowledge (知识库/RAG)** | 支持本地部署的 ChromaDB/LanceDB，可录入自有旅游攻略及指南，为智能体提供语义检索增强 (RAG)。 |
| **Custom Tools (自定义工具)** | 内置航班规划、住宿推荐、景点搜索等领域特定工具 (Toolkit)。 |

## 🏗️ 项目架构

```text
Traveler/
├── .env.example                # 环境变量配置模板
├── pyproject.toml              # 项目配置及依赖管理 (基于 Hatch)
├── data/                       # 运行时数据存储 (SQLite会话记录, ChromaDB向量数据, 导出报告等)
├── src/traveler/               # 核心源码目录
│   ├── agents/                 # 智能体定义 (规划师、研究员、预算师及团队组建)
│   ├── api/                    # FastAPI 后端服务 (应用工厂、路由、Schema)
│   ├── config/                 # Pydantic Settings 解析与 Loguru 日志配置
│   ├── core/                   # 核心基础设置 (模型工厂、数据库初始化、知识库管理)
│   │   └── mcp/                # 外部 MCP 客户端集成 (天气、Google路线等)
│   ├── knowledge_docs/         # 用于 RAG 向量化的本地知识文档存放区
│   ├── skills/                 # 智能体技能包 (Agno Skills 目录)
│   ├── tools/                  # 自定义工具函数及工作流辅助工具
│   ├── workflows/              # 标准化 Agno 工作流 (planning_workflow.py)
│   └── cli.py                  # Typer 命令行交互入口
└── tests/                      # Pytest 自动化测试用例
```

## 🚀 快速开始

### 1. 环境准备

推荐使用 **Python 3.12 或更高版本**。

```bash
# 创建并激活 conda 虚拟环境
conda create -n agno python=3.12
conda activate agno

# 安装项目依赖 (包含开发和测试工具)
pip install -e ".[dev]"
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入相关的 LLM Provider API Key 以及所需 MCP 服务的 API Key
# 支持 OpenAI, Anthropic 等多种大语言模型提供商
```

### 3. CLI 命令行使用

借助 Typer 框架提供了极佳的 CLI 交互体验。

```bash
# 启动交互式对话 (单智能体模式)
traveler chat

# 团队协作模式 (激活规划师 + 研究员 + 预算师)
traveler chat --mode team

# 标准工作流模式 (严格按 研究->预算->规划 执行)
traveler chat --mode workflow

# 指定大模型提供商及具体模型
traveler chat --provider anthropic --model-id claude-3-5-sonnet-20241022

# 离线/无MCP模式 (禁用外部网络和 MCP 依赖)
traveler chat --no-mcp
```

### 4. 启动 API 服务

Traveler 支持作为标准后端服务启动。

```bash
# 启动 FastAPI 服务
traveler serve

# 开发模式 (支持热重载)
traveler serve --reload

# API 调用示例 (cURL)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "帮我规划一个5天的东京旅行", "mode": "agent"}'
```

### 5. 补充本地知识库

如果您有特定的旅游攻略或私有数据：
1. 请将 Markdown 或 PDF 文档放入 `src/traveler/knowledge_docs/` 目录下。
2. 运行加载命令，将其切分并向量化进本地数据库：
```bash
traveler load-knowledge
```

## 📦 核心技术栈

- **[Agno](https://docs.agno.com)** - 智能体底层框架 (涵盖 Agent / Team / Workflow / MCP / Skills 等核心实现)
- **FastAPI / Uvicorn / Pydantic** - 现代化、高性能的 Web API 及数据验证
- **ChromaDB / LanceDB** - 向量数据库，支撑检索增强生成功能 (RAG)
- **SQLite / SQLAlchemy** - 对话记忆与长短期 Memory 存储中间件（生产可用 PostgreSQL 替换）
- **Typer & Rich** - 强大的 CLI 应用构建与终端 UI 美化
- **Loguru** - 开箱即用的高级日志系统

## 📄 开源协议

MIT License
