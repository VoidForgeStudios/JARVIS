from __future__ import annotations

from pathlib import Path

from app.core.permissions import PermissionLevel

from .base import ToolSpec


class DataFileTool:
    """Read files only inside JARVIS's configured data directory."""

    def __init__(self, data_dir: Path) -> None:
        self.root = data_dir.resolve()

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="read_file",
            description="Read a UTF-8 text file inside the JARVIS data directory.",
            parameters={"path": {"type": "string", "maxLength": 1000}},
            permission_level=PermissionLevel.SAFE,
        )

    def _safe_path(self, path: str) -> Path:
        candidate = (self.root / path).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PermissionError("File access outside the JARVIS data directory is blocked.")
        return candidate

    async def execute(self, *, path: str) -> str:
        candidate = self._safe_path(path)
        if not candidate.is_file():
            raise FileNotFoundError(path)
        if candidate.stat().st_size > 1_000_000:
            raise ValueError("File is too large for the text tool.")
        return candidate.read_text(encoding="utf-8")


class FindDataFilesTool(DataFileTool):
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="find_files",
            description="Find text files by filename pattern inside the JARVIS data directory.",
            parameters={"pattern": {"type": "string", "maxLength": 200}},
            permission_level=PermissionLevel.SAFE,
        )

    async def execute(self, *, pattern: str) -> str:
        if not pattern or len(pattern) > 200:
            raise ValueError("Invalid filename pattern.")
        matches = sorted(p for p in self.root.rglob(pattern) if p.is_file())
        return "\n".join(str(p.relative_to(self.root)) for p in matches[:100]) or "No matching files."
