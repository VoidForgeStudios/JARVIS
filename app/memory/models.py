from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MemoryCategory(StrEnum):
    USER_PROFILE = "USER_PROFILE"
    PREFERENCES = "PREFERENCES"
    PEOPLE = "PEOPLE"
    PROJECTS = "PROJECTS"
    DEVICES = "DEVICES"
    LOCATIONS = "LOCATIONS"
    ROUTINES = "ROUTINES"
    CONVERSATIONS = "CONVERSATIONS"
    TASKS = "TASKS"
    IMPORTANT_FACTS = "IMPORTANT_FACTS"


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(32), index=True)
    key: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(32), default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
