"""Router for URL redirect endpoint."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db, URL
from redis_client import get_redis

router = APIRouter()


@router.api_route("/{short_code}", methods=["GET", "HEAD"])
async def redirect_url(
    short_code: str,
    db: Session = Depends(get_db),
    format: Optional[str] = Query(None, description="Response format: 'json' for URL info, omit for redirect")
):
    """
    Redirect to original URL using short code, or return URL info as JSON.

    Args:
        short_code: Short code to look up
        db: Database session
        format: Optional query parameter. Use 'json' to get URL info instead of redirecting

    Returns:
        - If format=json: JSON with URL information
        - Otherwise: Redirect response to original URL

    Raises:
        HTTPException: If short code not found
    """
    redis_client = get_redis()
    cache_key = f"url:{short_code}"

    # Check cache first
    cached_url = redis_client.get(cache_key)
    if cached_url:
        original_url = cached_url
        from_cache = True
    else:
        # Cache miss - check database
        db_url = db.query(URL).filter(URL.short_code == short_code).first()

        if not db_url:
            raise HTTPException(status_code=404, detail="URL not found")

        original_url = db_url.original_url
        from_cache = False

        # Update cache with 24h TTL (86400 seconds)
        redis_client.setex(cache_key, 86400, original_url)

    # If format=json, return URL info instead of redirecting
    if format == "json":
        return {
            "short_code": short_code,
            "original_url": original_url,
            "will_redirect_to": original_url,
            "cached": from_cache
        }

    # Normal redirect behavior
    return RedirectResponse(url=original_url, status_code=302)

