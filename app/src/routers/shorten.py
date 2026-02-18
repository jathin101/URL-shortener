"""Router for URL shortening endpoint."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from database import get_db, URL
from schemas import URLCreate, URLResponse
from shortener import generate_short_code
from config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/shorten", response_model=URLResponse)
@limiter.limit("100/minute")
async def shorten_url(
    request: Request,
    url_data: URLCreate,
    db: Session = Depends(get_db)
):
    """
    Create a short URL.
    
    Args:
        request: FastAPI request object
        url_data: URL to shorten
        db: Database session
        
    Returns:
        Short URL response
    """
    # Generate unique short code
    short_code = generate_short_code()
    
    # Check for collision and regenerate if needed
    max_attempts = 10
    attempts = 0
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()
        attempts += 1
        if attempts >= max_attempts:
            short_code = generate_short_code(length=8)
            break
    
    # Save to database
    db_url = URL(
        short_code=short_code,
        original_url=str(url_data.url)
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # Return short URL
    return URLResponse(
        short_url=f"{settings.base_url}/{short_code}"
    )

