"""Abstract interfaces for the database layer and its repositories."""

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any

from sqlalchemy.orm import Session


class BaseDatabase(ABC):
    """Base class for database operations."""

    @abstractmethod
    def startup(self) -> None:
        """Initialize the database connection."""

    @abstractmethod
    def teardown(self) -> None:
        """Close the database connection."""

    @abstractmethod
    def get_session(self) -> AbstractContextManager[Session]:
        """Get a database session, to be used in a `with` block."""


class BaseRepository[ModelT](ABC):
    """Base repository pattern for data access.

    `ModelT` is the SQLAlchemy model handled by the repository,
    e.g. `class PaperRepository(BaseRepository[Paper])`.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def create(self, data: dict[str, Any]) -> ModelT:
        """Create a new record."""

    @abstractmethod
    def get_by_id(self, record_id: Any) -> ModelT | None:
        """Get a record by ID, or None if it does not exist."""

    @abstractmethod
    def update(self, record_id: Any, data: dict[str, Any]) -> ModelT | None:
        """Update a record by ID, or return None if it does not exist."""

    @abstractmethod
    def delete(self, record_id: Any) -> bool:
        """Delete a record by ID; return True if it was deleted."""

    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        """List records with pagination."""
