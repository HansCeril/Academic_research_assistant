"""Object storage settings (S3 API)."""

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class StorageSettings(BaseConfigSettings):
    """Object storage settings.

    Any S3-compatible service works: MinIO (local, on premise), Ceph,
    AWS S3, OVHcloud, Scaleway... Values are read from `STORAGE_*`
    variables, e.g. `STORAGE_BUCKET` sets `bucket`. Without access keys,
    boto3 resolves the credentials itself (profile, IAM role, Kubernetes
    workload identity).
    """

    model_config = SettingsConfigDict(env_prefix="STORAGE_")

    endpoint_url: str | None = Field(
        default=None,
        description="S3 API URL used by the services, e.g. http://minio:9000; "
        "None for AWS S3",
    )
    public_endpoint_url: str | None = Field(
        default=None,
        description="S3 API URL put in download links, reachable from the "
        "browser, e.g. http://localhost:9000; defaults to endpoint_url",
    )
    region: str = Field(
        default="us-east-1",
        description="Region of the bucket (MinIO uses us-east-1 by default)",
    )
    access_key: str | None = Field(default=None, description="Access key ID")
    secret_key: SecretStr | None = Field(default=None, description="Secret key")
    bucket: str = Field(
        default="cv-search-assistant",
        description="Bucket holding raw CVs, processed CVs, templates and exports",
    )
    raw_prefix: str = Field(
        default="cvs/raw/",
        description="Prefix where the ATS uploads raw CVs (PDF, DOCX)",
    )
    processed_prefix: str = Field(
        default="cvs/processed/",
        description="Prefix for extracted text and JSON profiles",
    )
    templates_prefix: str = Field(
        default="templates/",
        description="Prefix for client CV templates (.docx)",
    )
    exports_prefix: str = Field(
        default="exports/",
        description="Prefix for generated CVs (DOCX, PDF)",
    )
    presigned_url_ttl: int = Field(
        default=900,
        gt=0,
        le=3600,
        description="Lifetime of export download links, in seconds",
    )
