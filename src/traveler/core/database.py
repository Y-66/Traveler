"""数据库初始化 - Session / Memory / Knowledge 存储"""

from __future__ import annotations

from functools import lru_cache

from agno.db.sqlite import SqliteDb

from traveler.config.settings import DATA_DIR, get_settings


@lru_cache
def get_agent_db() -> SqliteDb:
    """获取 Agent 使用的数据库实例（SQLite）"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_file = str(DATA_DIR / "traveler.db")
    return SqliteDb(db_file=db_file)
