"""Configuration management using pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://urluser:urlpass@postgres:5432/urlshortener"
    
    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    
    # Application
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    base_url: str = "http://localhost"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

