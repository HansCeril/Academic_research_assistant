"""Redis (semantic cache) configuration settings."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class RedisSettings(BaseConfigSettings):
    """Redis configuration settings.

    Values are read from `REDIS_*` variables, e.g. `REDIS_URL` sets
    `url`.
    """

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis URL",
    )
    cache_enabled: bool = Field(
        default=True,
        description="Enable the semantic cache",
    )
    cache_ttl: int = Field(
        default=3600,
        gt=0,
        description="Lifetime of a cached answer, in seconds",
    )
    similarity_threshold: float = Field(
        default=0.95,
        gt=0,
        le=1,
        description="Minimum cosine similarity to reuse a cached answer",
    )
    max_entries: int = Field(
        default=200,
        gt=0,
        description="Cached entries kept per team and endpoint",
    )
