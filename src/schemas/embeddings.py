"""Embedding and re-ranking configuration settings."""

from typing import Literal

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class EmbeddingSettings(BaseConfigSettings):
    """Embedding configuration settings.

    Values are read from `EMBEDDINGS_*` variables, e.g.
    `EMBEDDINGS_PROVIDER` sets `provider`. TEI (bge-m3) runs in the
    stack, on any infrastructure; Bedrock is an AWS-only option. Both
    providers produce
    1024-dimension vectors, but vectors of different models are not
    comparable: reindex after switching provider.
    """

    model_config = SettingsConfigDict(env_prefix="EMBEDDINGS_")

    provider: Literal["tei", "bedrock"] = Field(
        default="tei",
        description="'tei' serves bge-m3 in the stack; 'bedrock' calls AWS",
    )
    dimension: int = Field(
        default=1024,
        gt=0,
        description="Vector size, must match the OpenSearch mapping",
    )
    bedrock_region: str = Field(
        default="eu-west-3",
        description="Bedrock region of the embedding model",
    )
    bedrock_model_id: str = Field(
        default="amazon.titan-embed-text-v2:0",
        description="Bedrock embedding model",
    )
    tei_url: str = Field(
        default="http://tei-embed:80",
        description="URL of the Text Embeddings Inference server",
    )
    batch_size: int = Field(
        default=16,
        ge=1,
        description="Texts sent per TEI request",
    )
    timeout: float = Field(
        default=30.0,
        gt=0,
        description="Request timeout in seconds",
    )


class RerankerSettings(BaseConfigSettings):
    """Re-ranking configuration settings.

    Values are read from `RERANKER_*` variables, e.g.
    `RERANKER_ENABLED` sets `enabled`. When disabled, candidates keep
    their fused (RRF) order.
    """

    model_config = SettingsConfigDict(env_prefix="RERANKER_")

    enabled: bool = Field(
        default=False,
        description="Re-rank with bge-reranker served by TEI",
    )
    url: str = Field(
        default="http://tei-rerank:80",
        description="URL of the TEI re-ranking server",
    )
    timeout: float = Field(
        default=30.0,
        gt=0,
        description="Request timeout in seconds",
    )
