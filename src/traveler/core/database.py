"""数据库初始化 - Session / Memory / Knowledge 存储"""

from __future__ import annotations

from functools import lru_cache

from agno.db.sqlite import SqliteDb

from traveler.config.settings import DATA_DIR


@lru_cache
def get_agent_db() -> SqliteDb:
    """获取 Agent 使用的数据库实例（SQLite）"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_file = str(DATA_DIR / "traveler.db")
    return SqliteDb(db_file=db_file)


@lru_cache
def get_workflow_db() -> SqliteDb:
    """获取 Workflow 使用的数据库实例"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_file = str(DATA_DIR / "traveler.db")
    return SqliteDb(db_file=db_file, session_table="workflow_sessions")


@lru_cache
def get_memory_db() -> SqliteDb:
    """获取 Memory 使用的数据库实例"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_file = str(DATA_DIR / "traveler.db")
    return SqliteDb(db_file=db_file, memory_table="traveler_memories")
