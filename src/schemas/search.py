"""Retrieval settings and the search, match and ask API models."""

from uuid import UUID

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from src.schemas.cv import Seniority
from src.services.config import BaseConfigSettings


class RetrievalSettings(BaseConfigSettings):
    """Retrieval configuration settings.

    Values are read from `RETRIEVAL_*` variables, e.g.
    `RETRIEVAL_RRF_K` sets `rrf_k`.
    """

    model_config = SettingsConfigDict(env_prefix="RETRIEVAL_")

    lexical_size: int = Field(default=50, gt=0, description="Chunks returned by BM25")
    vector_size: int = Field(default=50, gt=0, description="Chunks returned by kNN")
    rrf_k: int = Field(default=60, gt=0, description="Reciprocal rank fusion constant")
    rerank_candidates: int = Field(
        default=30, gt=0, description="Candidates sent to the re-ranker"
    )
    chunks_per_candidate: int = Field(
        default=3, gt=0, description="Chunks kept as evidence per candidate"
    )
    sql_candidate_limit: int = Field(
        default=5000,
        gt=0,
        description="Maximum candidates kept by the SQL pre-filter",
    )


class SearchFilters(BaseModel):
    """Structured criteria, extracted from the query or given directly."""

    skills: list[str] = Field(
        default_factory=list,
        description="Required skills, normalized names (e.g. 'Python')",
    )
    min_years_experience: float | None = Field(
        None, description="Minimum years of experience"
    )
    max_years_experience: float | None = Field(
        None, description="Maximum years of experience"
    )
    location: str | None = Field(None, description="City or region")
    languages: list[str] = Field(
        default_factory=list,
        description="Required spoken languages, in French (e.g. 'anglais')",
    )
    seniority: list[Seniority] = Field(
        default_factory=list, description="Accepted seniority levels"
    )

    def is_empty(self) -> bool:
        """Whether no criterion is set."""
        return not (
            self.skills
            or self.min_years_experience is not None
            or self.max_years_experience is not None
            or self.location
            or self.languages
            or self.seniority
        )


class QueryAnalysis(BaseModel):
    """Output of query understanding."""

    semantic_query: str = Field(
        ...,
        description="Query rewritten for semantic search: skills, "
        "missions and context, without filler words",
    )
    filters: SearchFilters = Field(default_factory=SearchFilters)


class SearchRequest(BaseModel):
    """Request of `/search`."""

    query: str = Field(
        ...,
        min_length=2,
        max_length=2000,
        examples=["Data engineer Spark AWS, 5 ans d'expérience, Paris"],
    )
    filters: SearchFilters | None = Field(
        None,
        description="Explicit filters; when null they are extracted from the query",
    )
    top_k: int = Field(10, ge=1, le=50)


class MatchRequest(BaseModel):
    """Request of `/match`: a job offer to match against the CVs."""

    offer: str = Field(..., min_length=20, max_length=20000)
    top_k: int = Field(10, ge=1, le=50)


class AskRequest(BaseModel):
    """Request of `/ask` (RAG question answering)."""

    question: str = Field(
        ...,
        min_length=2,
        max_length=2000,
        examples=["Qui a déjà migré un data lake vers AWS ?"],
    )
    top_k: int = Field(5, ge=1, le=20)


class Evidence(BaseModel):
    """One CV passage supporting a match."""

    chunk_id: str
    section: str
    text: str
    score: float


class ScoreExplanation(BaseModel):
    """Explainable score of a candidate."""

    score: int = Field(..., ge=0, le=100, description="Overall score")
    relevance: float = Field(
        ..., description="Semantic relevance, 0-1 (re-ranker or RRF)"
    )
    criteria_covered: list[str] = Field(default_factory=list)
    criteria_missing: list[str] = Field(default_factory=list)


class CandidateMatch(BaseModel):
    """One ranked candidate."""

    candidate_id: UUID
    headline: str | None
    location: str | None
    years_experience: float | None
    skills: list[str]
    score: ScoreExplanation
    evidence: list[Evidence]
    cv_url: str = Field(..., description="API path of the full profile")


class SearchResponse(BaseModel):
    """Response of `/search` and `/match`."""

    query: str
    analysis: QueryAnalysis
    results: list[CandidateMatch]
    cached: bool = False
    trace_id: str | None = None
