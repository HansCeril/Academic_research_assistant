import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.interfaces.postgres import PostgreSQLDatabase
from src.dependencies import get_settings
from src.routers import ping
from src.schemas.database import PostgreSQLSettings

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Open the database pool on startup and close it on shutdown."""
    database = PostgreSQLDatabase(PostgreSQLSettings())
    database.startup()
    app.state.database = database
    try:
        yield
    finally:
        database.teardown()


app = FastAPI(
    title="Academic Research Assistant",
    description=(
        "A FastAPI application that serves as an academic research "
        "assistant, providing tools and resources for researchers to "
        "streamline their workflow and enhance productivity."
    ),
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    contact={
        "name": " Hans CERIL",
        "email": "hansceril.devops@gmail.com",
    },
)


app.include_router(ping.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
