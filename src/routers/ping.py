import logging
from collections.abc import Callable

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from src.dependencies import DatabaseDep, SettingsDep
from src.schemas.health import HealthResponse, ServiceStatus

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    tags=["Health"]
)
def health_check(
    response: Response, settings: SettingsDep, database: DatabaseDep
) -> HealthResponse:
    """Check the API and its database connection.

    Declared as a sync function so FastAPI runs the blocking database
    call in its threadpool instead of blocking the event loop.
    """
    services: dict[str, ServiceStatus] = {}
    overall_status = "ok"

    def _check_service(
        name: str,
        check_func: Callable[[], ServiceStatus],
    ) -> None:
        """Run one service check and record its result.

        Any exception raised by the check marks the service as unhealthy
        instead of failing the whole endpoint; the traceback is logged.
        A non-healthy result also sets the overall status to "degraded".

        Args:
            name (str): Key of the service in the response (e.g. "database").
            check_func (Callable[[], ServiceStatus]): Function that checks
                the service and returns its status.
        """
        nonlocal overall_status
        try:
            result = check_func()
        # Any failure, whatever its type, means the service is down.
        except Exception:
            logger.exception("Health check failed for %s", name)
            result = ServiceStatus(
                status="unhealthy",
                message="Connection failed",
            )
        services[name] = result
        if result.status != "healthy":
            overall_status = "degraded"

    # Database check
    def _check_database() -> ServiceStatus:
        """Check that PostgreSQL accepts connections and runs a query.

        Returns:
            ServiceStatus: Healthy status if `SELECT 1` succeeds.

        Raises:
            SQLAlchemyError: If the database is unreachable or the query
                fails; handled by `_check_service`.
        """
        with database.get_session() as session:
            session.execute(text("SELECT 1"))
        return ServiceStatus(
            status="healthy",
            message="Connected successfully",
        )

    _check_service("database", _check_database)

    if overall_status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthResponse(
        status=overall_status,
        version=settings.app_version,
        environment=settings.environment,
        service_name=settings.service_name,
        services=services,
    )
