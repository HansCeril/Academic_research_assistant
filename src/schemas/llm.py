"""Claude (Anthropic API or Amazon Bedrock) configuration settings."""

from typing import Literal

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class LLMSettings(BaseConfigSettings):
    """Claude configuration settings.

    Values are read from `LLM_*` variables, e.g. `LLM_PROVIDER` sets
    `provider`. The Anthropic API key is read by the SDK itself from
    `ANTHROPIC_API_KEY`; Bedrock uses the boto3 credentials.
    """

    model_config = SettingsConfigDict(env_prefix="LLM_")

    provider: Literal["anthropic", "bedrock"] = Field(
        default="anthropic",
        description="'bedrock' keeps inference inside AWS (EU region)",
    )
    bedrock_region: str = Field(
        default="eu-west-3",
        description="Bedrock region, used when provider is 'bedrock'",
    )
    bedrock_model_prefix: str = Field(
        default="anthropic.",
        description="Prefix added to model IDs on Bedrock",
    )
    generation_model: str = Field(
        default="claude-sonnet-5-5",
        description="Model for answers and CV mapping",
    )
    extraction_model: str = Field(
        default="claude-haiku-5-5",
        description="Model for CV extraction and query understanding",
    )
    generation_effort: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Effort of the answer generator",
    )
    max_tokens: int = Field(
        default=16000,
        ge=1024,
        description="Maximum output tokens per request",
    )
    timeout: float = Field(
        default=120.0,
        gt=0,
        description="Request timeout in seconds",
    )
