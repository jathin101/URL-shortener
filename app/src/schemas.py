"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """Request schema for creating a short URL."""
    url: HttpUrl


class URLResponse(BaseModel):
    """Response schema for short URL creation."""
    short_url: str


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str
    database: str = "unknown"
    redis: str = "unknown"

