"""OpenSearch configuration settings."""

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class OpenSearchSettings(BaseConfigSettings):
    """OpenSearch configuration settings.

    Values are read from `OPENSEARCH_*` variables, e.g.
    `OPENSEARCH_HOST` sets `host`.
    """

    model_config = SettingsConfigDict(env_prefix="OPENSEARCH_")

    host: str = Field(
        default="http://localhost:9200",
        description="OpenSearch URL",
    )
    timeout: float = Field(
        default=5.0,
        gt=0,
        description="Request timeout in seconds",
    )
    index_name: str = Field(
        default="cv_chunks",
        description="Index of the CV chunks (BM25 + kNN)",
    )
    username: str | None = Field(
        default=None,
        description="Basic auth user (security plugin); None when disabled",
    )
    password: SecretStr | None = Field(default=None, description="Basic auth password")
    verify_certs: bool = Field(
        default=True,
        description="Verify the TLS certificate of an https:// host",
    )
