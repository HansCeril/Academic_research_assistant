from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Request

from src.database.interfaces.postgres import PostgreSQLDatabase
from src.services.config import Settings
from src.services.opensearch import OpenSearchClient


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


def get_database(request: Request) -> PostgreSQLDatabase:
    """Return the database opened by the app lifespan (see main.py)."""
    return request.app.state.database


def get_opensearch(request: Request) -> OpenSearchClient:
    """Return the OpenSearch client created by the app lifespan (see main.py)."""
    return request.app.state.opensearch


SettingsDep = Annotated[Settings, Depends(get_settings)]
DatabaseDep = Annotated[PostgreSQLDatabase, Depends(get_database)]
OpenSearchDep = Annotated[OpenSearchClient, Depends(get_opensearch)]
