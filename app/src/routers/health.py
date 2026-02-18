"""Router for health check endpoint."""
from fastapi import APIRouter

from schemas import HealthResponse
from database import check_db_health
from redis_client import check_redis_health

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check application health.
    
    Returns:
        Health status including database and Redis connectivity
    """
    db_healthy = check_db_health()
    redis_healthy = check_redis_health()
    
    overall_status = "healthy" if (db_healthy and redis_healthy) else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        database="healthy" if db_healthy else "unhealthy",
        redis="healthy" if redis_healthy else "unhealthy"
    )

