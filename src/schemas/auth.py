"""Authentication (OpenID Connect) settings and user model."""

from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings

Role = Literal["admin", "recruiter", "viewer"]


class AuthSettings(BaseConfigSettings):
    """Authentication settings, for any OpenID Connect provider.

    Values are read from `AUTH_*` variables, e.g. `AUTH_ENABLED` sets
    `enabled`. When disabled (local development only), every request
    acts as an admin of `dev_team`.
    """

    model_config = SettingsConfigDict(env_prefix="AUTH_")

    enabled: bool = Field(
        default=False,
        description="Verify the access token (JWT) of every request",
    )
    issuer: str = Field(
        default="http://localhost:8080/realms/cv-search",
        description="Expected `iss` of the tokens (Keycloak realm URL, ...)",
    )
    jwks_url: str | None = Field(
        default=None,
        description="URL of the signing keys; found through the issuer's "
        "discovery document when not set. Needed when the API reaches the "
        "provider by another host name than the issuer (Docker, Kubernetes)",
    )
    audience: str = Field(
        default="cv-search-api",
        description="Expected `aud` of the tokens: this API",
    )
    groups_claim: str = Field(
        default="groups",
        description="Claim listing the user's groups ('cognito:groups' on Cognito)",
    )
    team_group_prefix: str = Field(
        default="team-",
        description="Groups starting with this prefix are teams",
    )
    dev_team: str = Field(
        default="default",
        description="Team used when authentication is disabled",
    )


class CurrentUser(BaseModel):
    """Authenticated user, built from the access token."""

    sub: str = Field(..., description="User ID at the identity provider")
    username: str = Field(..., description="Username")
    team: str = Field(..., description="RH team owning the data")
    roles: set[Role] = Field(
        default_factory=set,
        description="Roles from the groups",
    )
