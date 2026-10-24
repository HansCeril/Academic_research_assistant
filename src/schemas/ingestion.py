"""Ingestion settings and the results of the ingestion Lambda."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class IngestionSettings(BaseConfigSettings):
    """Ingestion configuration settings.

    Values are read from `INGESTION_*` variables, e.g.
    `INGESTION_MIN_TEXT_CHARS` sets `min_text_chars`.
    """

    model_config = SettingsConfigDict(env_prefix="INGESTION_")

    min_text_chars: int = Field(
        default=300,
        ge=0,
        description="Below this length a PDF is treated as scanned and read by OCR",
    )
    ocr_languages: str = Field(
        default="fra+eng",
        description="Tesseract languages, installed in the image",
    )
    ocr_dpi: int = Field(
        default=300,
        ge=72,
        description="Resolution of the pages rendered for OCR",
    )
    ner_enabled: bool = Field(
        default=True,
        description="Detect and redact person names with spaCy",
    )
    ner_model: str = Field(
        default="fr_core_news_md",
        description="spaCy model of the name detection, installed with the "
        "dependencies",
    )
    default_team: str = Field(
        default="default",
        description="Team used when the S3 object has no 'team' tag",
    )


class IngestResponse(BaseModel):
    """Result of the ingestion of one CV."""

    key: str = Field(..., description="S3 key of the raw CV")
    status: Literal["ingested", "duplicate", "skipped"] = Field(
        ...,
        description="'duplicate' when the same file was already ingested",
    )
    candidate_id: UUID | None = Field(None, description="Candidate ID")
    chunks: int = Field(0, description="Number of indexed chunks")
    ocr_used: bool = Field(False, description="Whether OCR was used")
    message: str | None = Field(None, description="Details")


class ReindexResponse(BaseModel):
    """Result of an OpenSearch rebuild from PostgreSQL."""

    candidates: int = Field(..., description="Candidates reindexed")
    chunks: int = Field(..., description="Chunks reindexed")


class IngestionJobResponse(BaseModel):
    """Ingestion status of one version of a raw CV."""

    model_config = ConfigDict(from_attributes=True)

    source_key: str
    status: Literal["queued", "ingested", "duplicate", "skipped", "failed"]
    attempts: int
    message: str | None
    created_at: datetime
    updated_at: datetime
