"""Candidate profile models.

`CVProfile` is the structured output requested from Claude during
ingestion, so field descriptions double as extraction instructions.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

Seniority = Literal["junior", "confirmed", "senior", "expert"]


class Experience(BaseModel):
    """One professional experience."""

    title: str = Field(..., description="Job title as written in the CV")
    company: str | None = Field(None, description="Employer or client")
    start_date: str | None = Field(None, description="Start date as YYYY-MM, or YYYY")
    end_date: str | None = Field(
        None, description="End date as YYYY-MM or YYYY, null if current"
    )
    duration_months: int | None = Field(
        None, description="Duration in months, only if computable"
    )
    description: str = Field(
        ..., description="Missions and achievements, faithful to the CV"
    )
    skills: list[str] = Field(
        default_factory=list,
        description="Technologies and skills used in this experience",
    )


class Education(BaseModel):
    """One degree or training."""

    degree: str = Field(..., description="Degree or training name")
    institution: str | None = Field(None, description="School")
    year: int | None = Field(None, description="Graduation year")


class LanguageSkill(BaseModel):
    """One spoken language."""

    language: str = Field(..., description="Language name in French")
    level: str | None = Field(
        None, description="Level as written (e.g. C1, courant, natif)"
    )


class CVProfile(BaseModel):
    """Professional profile extracted from a CV.

    Contains no contact details: they are removed from the text before
    extraction and stored separately.
    """

    headline: str = Field(
        ..., description="Current or target job title, e.g. 'Data Engineer'"
    )
    summary: str = Field(
        ..., description="Two or three sentence summary of the profile"
    )
    location: str | None = Field(
        None, description="City of residence or work, if stated"
    )
    years_experience: float | None = Field(
        None, description="Total years of professional experience"
    )
    seniority: Seniority | None = Field(
        None,
        description="junior <3y, confirmed 3-6y, senior 6-10y, expert >10y",
    )
    skills: list[str] = Field(
        default_factory=list,
        description="All technical and functional skills, deduplicated",
    )
    experiences: list[Experience] = Field(
        default_factory=list,
        description="Experiences, most recent first",
    )
    education: list[Education] = Field(default_factory=list)
    languages: list[LanguageSkill] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ContactInfo(BaseModel):
    """Contact details detected in a CV, never sent to the LLM."""

    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    links: list[str] = Field(default_factory=list)


class CandidateSummary(BaseModel):
    """Candidate in a list (no contact details)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    headline: str | None
    location: str | None
    years_experience: float | None
    seniority: str | None
    skills: list[str]
    updated_at: datetime


class CandidatePage(BaseModel):
    """A page of the filtered candidate list."""

    total: int = Field(..., description="Candidates matching the filters")
    items: list[CandidateSummary]


class FacetValue(BaseModel):
    """A filter value and the number of candidates having it."""

    value: str
    count: int


class CandidateFacets(BaseModel):
    """Values present in the team's candidates, to suggest filters."""

    skills: list[FacetValue]
    languages: list[FacetValue]
    locations: list[FacetValue]
    seniority: list[FacetValue]


class UploadResponse(BaseModel):
    """A raw CV stored for ingestion."""

    key: str = Field(..., description="Storage key under the raw prefix")


class CandidateResponse(BaseModel):
    """Candidate returned by `/cv/{id}`."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    team: str
    source_key: str
    full_name: str | None
    email: str | None
    phone: str | None
    headline: str | None
    location: str | None
    years_experience: float | None
    seniority: str | None
    skills: list[str]
    languages: list[str]
    profile: CVProfile
    created_at: datetime
    updated_at: datetime
