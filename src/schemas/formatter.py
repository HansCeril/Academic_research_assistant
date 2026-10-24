"""CV formatter settings and API models."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings

MISSING_VALUE = "[À COMPLÉTER]"


class GotenbergSettings(BaseConfigSettings):
    """Gotenberg (DOCX to PDF) configuration settings.

    Values are read from `GOTENBERG_*` variables, e.g. `GOTENBERG_URL`
    sets `url`.
    """

    model_config = SettingsConfigDict(env_prefix="GOTENBERG_")

    url: str = Field(
        default="http://localhost:3000",
        description="Gotenberg URL",
    )
    timeout: float = Field(
        default=60.0,
        gt=0,
        description="Conversion timeout in seconds",
    )


class TemplateResponse(BaseModel):
    """A client CV template."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    team: str
    name: str
    version: int
    placeholders: list[str]
    created_by: str
    created_at: datetime


class FieldMapping(BaseModel):
    """Value of one template placeholder, mapped from the profile."""

    name: str = Field(..., description="Placeholder name")
    value: str | None = Field(
        None,
        description="Value taken from the profile, null if the profile "
        "does not contain it",
    )
    source: str | None = Field(
        None,
        description="Profile field the value comes from, e.g. 'experiences[0].company'",
    )


class TemplateMapping(BaseModel):
    """Mapping of all custom placeholders of a template."""

    fields: list[FieldMapping]


class FormatRequest(BaseModel):
    """Request of `/format`: render a candidate into a template."""

    candidate_id: UUID
    template_id: UUID
    anonymize: bool = Field(
        True,
        description="Replace the name by initials and hide contact details",
    )


class ReviewRequest(BaseModel):
    """Recruiter review of a generated CV."""

    approved: bool = Field(..., description="Validate the export")
    overrides: dict[str, str] = Field(
        default_factory=dict,
        description="Placeholder values corrected by the recruiter",
    )


class ExportResponse(BaseModel):
    """A generated CV."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_id: UUID
    template_id: UUID
    status: Literal["draft", "validated"]
    missing_fields: list[str]
    mapping: dict[str, str | None]
    created_by: str
    created_at: datetime
    validated_at: datetime | None


class DownloadResponse(BaseModel):
    """Presigned download link of an export."""

    url: str
    format: Literal["docx", "pdf"]
    expires_in: int
