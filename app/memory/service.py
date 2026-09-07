from __future__ import annotations

from sqlalchemy import delete, or_, select

from .database import MemoryDatabase
from .models import Memory, MemoryCategory


class MemoryService:
    """Explicit, user-controlled persistent memory. Nothing is saved implicitly."""

    def __init__(self, database: MemoryDatabase) -> None:
        self.database = database

    def remember(self, category: MemoryCategory, key: str, content: str, source: str = "user") -> Memory:
        key = key.strip()
        content = content.strip()
        if not key or not content:
            raise ValueError("Memory key and content are required.")
        with self.database.session() as session:
            existing = session.scalar(
                select(Memory).where(Memory.category == category.value, Memory.key == key)
            )
            if existing:
                existing.content = content
                existing.source = source
                memory = existing
            else:
                memory = Memory(category=category.value, key=key, content=content, source=source)
                session.add(memory)
            session.commit()
            session.refresh(memory)
            return memory

    def forget(self, key: str, category: MemoryCategory | None = None) -> int:
        with self.database.session() as session:
            statement = delete(Memory).where(Memory.key == key.strip())
            if category:
                statement = statement.where(Memory.category == category.value)
            result = session.execute(statement)
            session.commit()
            return result.rowcount or 0

    def search(self, query: str, limit: int = 10) -> list[Memory]:
        terms = [term for term in query.lower().split() if term]
        if not terms:
            return []
        with self.database.session() as session:
            clauses = []
            for term in terms:
                pattern = f"%{term}%"
                clauses.append(or_(Memory.key.ilike(pattern), Memory.content.ilike(pattern)))
            return list(session.scalars(select(Memory).where(or_(*clauses)).limit(limit)))

    def list_recent(self, limit: int = 20) -> list[Memory]:
        with self.database.session() as session:
            return list(session.scalars(select(Memory).order_by(Memory.updated_at.desc()).limit(limit)))
