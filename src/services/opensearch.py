"""OpenSearch client used by the application."""

import logging
from typing import Any

from opensearchpy import OpenSearch

from src.schemas.opensearch import OpenSearchSettings

logger = logging.getLogger(__name__)


class OpenSearchClient:
    """Thin wrapper around the OpenSearch client."""

    def __init__(self, config: OpenSearchSettings) -> None:
        self.config = config
        self.client = OpenSearch(hosts=[config.host], timeout=config.timeout)
        logger.info("OpenSearch client configured for %s", config.host)

    def cluster_health(self) -> dict[str, Any]:
        """Return the cluster health (name, status green/yellow/red, ...).

        Raises:
            opensearchpy.exceptions.OpenSearchException: If the cluster
                is unreachable or the request fails.
        """
        return self.client.cluster.health()

    def close(self) -> None:
        """Close the HTTP connections."""
        self.client.close()
        logger.info("OpenSearch client closed")
