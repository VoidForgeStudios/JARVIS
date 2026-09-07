from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment and optional .env file."""

    model_config = SettingsConfigDict(
        env_prefix="JARVIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "JARVIS"
    user_name: str = "User"
    user_title: str = ""
    response_style: str = "concise"
    llm_provider: str = "anthropic"
    llm_model: str = ""
    log_level: str = "INFO"
    data_dir: Path = Field(default=Path("data"))
    require_confirmation_for_destructive: bool = True

    def ensure_data_dir(self) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir
