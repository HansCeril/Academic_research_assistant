from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ServiceStatus(BaseModel):
    """Individual service status."""

    status: Literal["healthy", "unhealthy"] = Field(
        ...,
        description="Service status",
        examples=["healthy"],
    )
    message: str | None = Field(
        None,
        description="Status message",
        examples=["Connected successfully"],
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "version": "0.1.0",
                "environment": "development",
                "service_name": "research-assistant-api",
                "services": {
                    "database": {
                        "status": "healthy",
                        "message": "Connected successfully",
                    },
                },
            }
        }
    )

    status: Literal["ok", "degraded"] = Field(
        ...,
        description="Overall health status",
        examples=["ok"],
    )
    version: str = Field(
        ...,
        description="Application version",
        examples=["0.1.0"],
    )
    environment: Literal["development", "staging", "production"] = Field(
        ...,
        description="Deployment environment",
        examples=["development"],
    )
    service_name: str = Field(
        ...,
        description="Service identifier",
        examples=["research-assistant-api"],
    )
    services: dict[str, ServiceStatus] | None = Field(
        None,
        description="Individual service statuses",
    )
