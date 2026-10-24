"""Request of the recruiter agent."""

from uuid import UUID

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """One message to the recruiter agent."""

    message: str = Field(
        ...,
        min_length=2,
        max_length=4000,
        examples=[
            "Trouve un data engineer Spark/AWS à Paris et compare les 3 meilleurs"
        ],
    )
    conversation_id: UUID | None = Field(
        None,
        description="Conversation to continue; a new one is started when absent",
    )
