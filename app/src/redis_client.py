"""Redis client for caching and rate limiting."""
import redis
from config import settings

# Create Redis connection pool
redis_pool = redis.ConnectionPool(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
    max_connections=50
)


def get_redis():
    """Get Redis client instance."""
    return redis.Redis(connection_pool=redis_pool)


def check_redis_health():
    """Check if Redis connection is healthy."""
    try:
        client = get_redis()
        client.ping()
        return True
    except Exception:
        return False

