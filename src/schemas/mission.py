"""Matching of a client's mission (job ad) against the team's CVs."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

RequirementCategory = Literal[
    "compétence",
    "expérience",
    "domaine",
    "langue",
    "localisation",
    "certification",
    "autre",
]
CheckStatus = Literal["met", "partial", "missing"]
Verdict = Literal["excellent", "good", "partial", "weak"]


class Requirement(BaseModel):
    """One requirement of the mission."""

    label: str = Field(
        ...,
        description="Short, checkable requirement in French, e.g. '5 ans de Python', "
        "'Anglais courant', 'Expérience dans la banque'",
    )
    category: RequirementCategory


class MissionRequirements(BaseModel):
    """Requirements extracted from a job ad by Claude."""

    title: str = Field(..., description="Title of the mission or role, in French")
    summary: str = Field(..., description="Context of the mission in 2 sentences")
    must_have: list[Requirement] = Field(
        default_factory=list, description="Requirements the ad states as mandatory"
    )
    nice_to_have: list[Requirement] = Field(
        default_factory=list, description="Requirements stated as a plus"
    )
    ignored_criteria: list[str] = Field(
        default_factory=list,
        description="Discriminatory criteria of the ad that were not kept "
        "(age, gender, origin, health, family status...)",
    )
    search_query: str = Field(
        ...,
        description="Dense description of the ideal profile for a semantic search: "
        "role, skills, missions, sector",
    )


class RequirementCheck(BaseModel):
    """How a candidate meets one requirement."""

    requirement: str = Field(..., description="Label of the requirement, unchanged")
    status: CheckStatus
    evidence: str | None = Field(
        None,
        description="Short paraphrase of the profile supporting the status; "
        "null if missing",
    )


class CandidateAssessment(BaseModel):
    """Claude's assessment of one candidate against the requirements."""

    checks: list[RequirementCheck] = Field(
        ..., description="One check per requirement, in the order given"
    )
    strengths: list[str] = Field(default_factory=list, description="At most 3")
    gaps: list[str] = Field(default_factory=list, description="At most 3")
    summary: str = Field(..., description="Fit with the mission, 2 sentences in French")


class MissionRequest(BaseModel):
    """A job ad pasted by the recruiter."""

    offer: str = Field(..., min_length=20, max_length=20000)
    top_k: int = Field(5, ge=1, le=10, description="Candidates to return")


class ScoredCheck(RequirementCheck):
    """A check, with whether its requirement is mandatory."""

    must_have: bool


class MissionCandidate(BaseModel):
    """A candidate assessed against the mission."""

    candidate_id: UUID
    headline: str | None
    location: str | None
    years_experience: float | None
    fit_score: int = Field(..., ge=0, le=100, description="Computed from the checks")
    verdict: Verdict
    must_have_met: int
    must_have_total: int
    checks: list[ScoredCheck]
    strengths: list[str]
    gaps: list[str]
    summary: str


class MissionResponse(BaseModel):
    """Requirements of the mission and the best candidates."""

    requirements: MissionRequirements
    candidates: list[MissionCandidate]
    shortlisted: int = Field(..., description="Candidates assessed")
    trace_id: str | None = None
