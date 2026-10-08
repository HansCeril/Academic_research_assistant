from typing import Literal
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"


class BaseConfigSettings(BaseSettings):
    """Provide shared configuration for application settings.

    Settings are loaded from `.env` files, ignore extra values, and are
    immutable after initialization. Nested environment variables use `__`
    as their delimiter, and variable names are case-insensitive.
    """
    model_config = SettingsConfigDict(
        env_file=[".env", str(ENV_FILE_PATH)],
        extra="ignore",
        frozen=True,
        env_nested_delimiter="__",
        case_sensitive=False,
    )


class Settings(BaseConfigSettings):
    """Define the application-wide settings and their defaults.

    Attributes:
        app_version: Version of the application.
        debug: Whether debug mode is enabled.
        environment: Deployment environment for the application.
        service_name: Name identifying this service.
    """
    app_version: str = "0.1.0"
    debug: bool = True
    environment: Literal[
        "development", "staging", "production"
    ] = "development"
    service_name: str = "research-assistant-api"
