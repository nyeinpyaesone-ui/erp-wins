"""
ERP Platform — Configuration Management

Externalized configuration using Pydantic Settings.
Configuration is validated once during startup.
Secrets must never be hard-coded or committed.
"""

from functools import lru_cache
from typing import List

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    app_name: str = Field(default="ERP Platform", description="Application name")
    app_env: str = Field(default="development", description="Environment (development, staging, production)")
    app_debug: bool = Field(default=False, description="Debug mode")
    app_log_level: str = Field(default="INFO", description="Log level")
    app_secret_key: str = Field(description="Secret key for signing (JWT, sessions, etc.)")

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API port")
    api_workers: int = Field(default=4, ge=1, description="Number of Uvicorn workers")
    api_cors_origins: List[str] = Field(default_factory=list, description="Allowed CORS origins")

    # -------------------------------------------------------------------------
    # PostgreSQL
    # -------------------------------------------------------------------------
    database_url: PostgresDsn = Field(description="PostgreSQL connection URL")
    db_pool_size: int = Field(default=20, ge=1, le=100, description="Connection pool size")
    db_max_overflow: int = Field(default=10, ge=0, le=50, description="Max overflow connections")
    db_pool_timeout: int = Field(default=30, ge=1, description="Pool timeout in seconds")
    db_pool_recycle: int = Field(default=1800, ge=60, description="Pool recycle time in seconds")

    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    redis_url: RedisDsn = Field(description="Redis connection URL")
    redis_password: str = Field(default="", description="Redis password (optional)")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis database number")

    # -------------------------------------------------------------------------
    # Celery
    # -------------------------------------------------------------------------
    celery_broker_url: RedisDsn = Field(description="Celery broker URL")
    celery_result_backend: RedisDsn = Field(description="Celery result backend URL")

    # -------------------------------------------------------------------------
    # Ollama (Local LLM)
    # -------------------------------------------------------------------------
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    ollama_model: str = Field(default="llama3.2", description="Default Ollama model")
    ollama_timeout: int = Field(default=60, ge=10, description="Ollama request timeout in seconds")

    # -------------------------------------------------------------------------
    # Observability
    # -------------------------------------------------------------------------
    prometheus_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, ge=1, le=65535, description="Metrics server port")

    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    jwt_algorithm: str = Field(default="HS256", description="JWT signing algorithm")
    jwt_expiration_minutes: int = Field(default=30, ge=1, description="JWT expiration in minutes")
    rate_limit_per_minute: int = Field(default=60, ge=1, description="Rate limit per minute")

    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------
    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"app_env must be one of {allowed}")
        return v

    @field_validator("app_log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in allowed:
            raise ValueError(f"app_log_level must be one of {allowed}")
        return v

    @field_validator("app_secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if not v or v == "change-me" or len(v) < 32:
            raise ValueError("app_secret_key must be a secure random value (min 32 chars)")
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Settings are loaded once and cached for the application lifetime.
    This ensures configuration is validated once during startup.
    """
    return Settings()
