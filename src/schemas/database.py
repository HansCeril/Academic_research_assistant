"""PostgreSQL configuration settings."""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class PostgreSQLSettings(BaseConfigSettings):
    """PostgreSQL configuration settings.

    Values are read from `POSTGRES_*` variables, e.g.
    `POSTGRES_DATABASE_URL` sets `database_url`.
    """

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    database_url: str = Field(
        default=(
            "postgresql+psycopg://research-assistant_user:"
            "research-assistant_password@localhost:5432/research-assistant_db"
        ),
        description="PostgreSQL database URL",
    )
    echo_sql: bool = Field(
        default=False,
        description="Enable SQL query logging",
    )
    pool_size: int = Field(
        default=20,
        ge=1,
        description="Database connection pool size",
    )
    max_overflow: int = Field(
        default=0,
        ge=0,
        description="Maximum pool overflow",
    )
