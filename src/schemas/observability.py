"""Langfuse (tracing, evaluation) configuration settings."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class LangfuseSettings(BaseConfigSettings):
    """Langfuse configuration settings.

    Values are read from `LANGFUSE_*` variables, e.g.
    `LANGFUSE_PUBLIC_KEY` sets `public_key`. Tracing is disabled when
    the keys are missing.
    """

    model_config = SettingsConfigDict(env_prefix="LANGFUSE_")

    public_key: str | None = Field(default=None, description="Public key")
    secret_key: str | None = Field(default=None, description="Secret key")
    host: str = Field(
        default="https://cloud.langfuse.com",
        description="Langfuse URL (EU cloud by default)",
    )

    @property
    def enabled(self) -> bool:
        """Whether both keys are set."""
        return bool(self.public_key and self.secret_key)
