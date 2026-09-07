from pathlib import Path

import pytest

from app.memory.database import MemoryDatabase
from app.memory.models import MemoryCategory
from app.memory.parser import parse_forget, parse_remember
from app.memory.service import MemoryService


def test_memory_round_trip(tmp_path: Path):
    memory = MemoryService(MemoryDatabase(tmp_path))
    saved = memory.remember(MemoryCategory.PREFERENCES, "coffee", "black")
    assert saved.key == "coffee"
    assert memory.search("black")[0].content == "black"
    assert memory.forget("coffee") == 1
    assert memory.search("black") == []


def test_remember_updates_same_key(tmp_path: Path):
    memory = MemoryService(MemoryDatabase(tmp_path))
    memory.remember(MemoryCategory.PREFERENCES, "coffee", "black")
    memory.remember(MemoryCategory.PREFERENCES, "coffee", "espresso")
    results = memory.search("coffee")
    assert len(results) == 1
    assert results[0].content == "espresso"


def test_explicit_parser():
    category, key, content = parse_remember("remember PREFERENCES coffee = black")
    assert category is MemoryCategory.PREFERENCES
    assert key == "coffee"
    assert content == "black"
    assert parse_forget("forget coffee") == "coffee"


def test_invalid_parser():
    with pytest.raises(ValueError):
        parse_remember("remember preferences coffee")
