"""PostgreSQL implementation of the database interface."""

import logging
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.database.interfaces.base import BaseDatabase
from src.schemas.database import PostgreSQLSettings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""


class PostgreSQLDatabase(BaseDatabase):
    """PostgreSQL database implementation."""

    def __init__(self, config: PostgreSQLSettings) -> None:
        self.config = config
        self.engine: Engine | None = None
        self.session_factory: sessionmaker[Session] | None = None

    def startup(self) -> None:
        """Initialize the database connection and create missing tables."""
        try:
            self.engine = create_engine(
                self.config.database_url,
                echo=self.config.echo_sql,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_pre_ping=True,  # Verify connections before use
                connect_args={"connect_timeout": 5},
            )
            # URL without the password, safe to log
            logger.info(
                "Connecting to PostgreSQL at %s",
                self.engine.url.render_as_string(hide_password=True),
            )

            self.session_factory = sessionmaker(
                bind=self.engine, expire_on_commit=False
            )

            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")

            # Create tables if they don't exist (idempotent operation).
            # Models must be imported before this point to be registered on Base.
            existing_tables = set(inspect(self.engine).get_table_names())
            Base.metadata.create_all(bind=self.engine)
            # New inspector: the first one caches its results
            updated_tables = set(inspect(self.engine).get_table_names())

            if new_tables := updated_tables - existing_tables:
                logger.info("Created new tables: %s", ", ".join(sorted(new_tables)))
            else:
                logger.info("All tables already exist - no new tables created")

            logger.info(
                "PostgreSQL database '%s' initialized, tables: %s",
                self.engine.url.database,
                ", ".join(sorted(updated_tables)) or "None",
            )

        except Exception:
            logger.exception("Failed to initialize PostgreSQL database")
            raise

    def teardown(self) -> None:
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.session_factory = None
            logger.info("PostgreSQL database connections closed")

    @contextmanager
    def get_session(self) -> Generator[Session]:
        """Get a database session, rolled back on error and always closed."""
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call startup() first.")

        with self.session_factory() as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise
