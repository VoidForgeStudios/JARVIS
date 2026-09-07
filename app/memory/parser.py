from __future__ import annotations

from app.memory.models import MemoryCategory


def parse_remember(text: str) -> tuple[MemoryCategory, str, str]:
    """Parse: remember <CATEGORY> <key> = <content>."""
    body = text.strip()[len("remember "):].strip()
    if "=" not in body:
        raise ValueError("Use: remember <CATEGORY> <key> = <content>")
    left, content = body.split("=", 1)
    parts = left.strip().split(None, 1)
    if len(parts) != 2:
        raise ValueError("Use: remember <CATEGORY> <key> = <content>")
    category = MemoryCategory(parts[0].upper())
    key = parts[1].strip()
    content = content.strip()
    if not key or not content:
        raise ValueError("Memory key and content are required.")
    return category, key, content


def parse_forget(text: str) -> str:
    key = text.strip()[len("forget "):].strip()
    if not key:
        raise ValueError("Use: forget <key>")
    return key
