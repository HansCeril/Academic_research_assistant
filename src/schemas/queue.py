"""Message queue (RabbitMQ) settings of the ingestion."""

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from src.services.config import BaseConfigSettings


class QueueSettings(BaseConfigSettings):
    """RabbitMQ settings.

    Values are read from `QUEUE_*` variables, e.g. `QUEUE_URL` sets
    `url`. The exchanges and queues are declared by RabbitMQ itself
    (docker/rabbitmq/definitions.json), not by the application.
    """

    model_config = SettingsConfigDict(env_prefix="QUEUE_")

    url: SecretStr = Field(
        default=SecretStr("amqp://cv_search:cv_search@localhost:5672/%2F"),
        description="AMQP URL, credentials included",
    )
    exchange: str = Field(
        default="cv.ingestion",
        description="Exchange receiving the CVs to ingest",
    )
    routing_key: str = Field(default="cv.raw", description="Routing key of the CVs")
    queue: str = Field(
        default="cv.ingestion",
        description="Queue consumed by the workers",
    )
    dead_letter_queue: str = Field(
        default="cv.ingestion.dlq",
        description="Queue of the CVs that failed `max_attempts` times",
    )
    max_attempts: int = Field(
        default=3,
        ge=1,
        description="Attempts before a CV goes to the dead-letter queue",
    )
    scan_interval: int = Field(
        default=60,
        ge=5,
        description="Seconds between two scans of the raw CVs",
    )
