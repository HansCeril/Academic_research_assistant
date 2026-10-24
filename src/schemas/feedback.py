"""Recruiter feedback API models."""

from uuid import UUID

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    """Feedback on the relevance of a candidate or an answer."""

    trace_id: str | None = Field(
        None, description="Trace returned by /search, /match or /ask"
    )
    query: str = Field(..., max_length=20000)
    candidate_id: UUID | None = None
    rating: int = Field(
        ..., ge=-1, le=1, description="-1 not relevant, 0 neutral, 1 relevant"
    )
    comment: str | None = Field(None, max_length=2000)


class FeedbackResponse(BaseModel):
    """Stored feedback."""

    id: UUID
