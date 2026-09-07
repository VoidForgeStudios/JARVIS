from pathlib import Path

from pydantic import Field, SecretStr
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
    personality: str = "calm, intelligent, concise, slightly witty, professional, helpful"
    response_style: str = "concise"
    llm_provider: str = "mock"
    llm_model: str = "mock-1"
    anthropic_api_key: SecretStr | None = None
    llm_temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    llm_max_tokens: int = Field(default=1024, ge=1, le=16384)
    log_level: str = "INFO"
    data_dir: Path = Field(default=Path("data"))
    require_confirmation_for_destructive: bool = True

    api_token: SecretStr | None = None
    cors_origins: str = ""

    def ensure_data_dir(self) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir

    def allowed_cors_origins(self) -> list[str]:
        return [origin.strip().rstrip("/") for origin in self.cors_origins.split(",") if origin.strip()]
