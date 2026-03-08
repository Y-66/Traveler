"""知识库初始化 - 向量数据库 + 文档知识管理"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

from traveler.config.settings import DATA_DIR, get_settings

# 旅游知识文档目录
KNOWLEDGE_DOCS_DIR = Path(__file__).resolve().parent.parent / "knowledge_docs"


@lru_cache
def get_travel_knowledge() -> Knowledge:
    """创建旅游知识库实例"""
    settings = get_settings()

    vector_db = ChromaDb(
        collection="travel_knowledge",
        path=settings.vector_db_path,
    )

    knowledge = Knowledge(vector_db=vector_db)
    return knowledge


def load_knowledge_documents() -> None:
    """加载旅游知识文档到向量数据库"""
    knowledge = get_travel_knowledge()
    docs_dir = KNOWLEDGE_DOCS_DIR

    if not docs_dir.exists():
        docs_dir.mkdir(parents=True, exist_ok=True)
        return

    # 加载目录中的所有 markdown / txt 文件
    for doc_path in docs_dir.glob("**/*.md"):
        knowledge.insert(file=str(doc_path))

    for doc_path in docs_dir.glob("**/*.txt"):
        knowledge.insert(file=str(doc_path))
