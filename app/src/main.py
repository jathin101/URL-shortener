"""Main FastAPI application."""
import logging
import time
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from routers import shorten, redirect, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="URL Shortener",
    description="Production-ready URL shortener with caching and monitoring",
    version="1.0.0"
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and track latency."""
    start_time = time.time()

    # Log request
    logger.info(f"{request.method} {request.url.path} - Client: {request.client.host}")

    # Process request
    response = await call_next(request)

    # Calculate latency
    latency = time.time() - start_time

    # Log response
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Latency: {latency:.3f}s"
    )

    return response


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(shorten.router, tags=["URL Shortener"])
app.include_router(redirect.router, tags=["Redirect"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "URL Shortener API",
        "docs": "/docs",
        "health": "/health"
    }

