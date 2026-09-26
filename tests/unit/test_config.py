"""
ERP Platform — Configuration Unit Tests

Tests for settings validation and loading.
"""

import os
import pytest

from app.config import Settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Clear settings cache before each test."""
    from app.config import get_settings
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_loads_from_env():
    """Settings load from environment variables."""
    os.environ["APP_SECRET_KEY"] = "test-secret-key-for-testing-minimum-32-chars!!"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://erp:test@localhost:5432/erp_test"
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    os.environ["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
    os.environ["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
    
    settings = Settings()
    
    assert settings.app_name == "ERP Platform"
    assert settings.app_env == "development"
    assert settings.api_port == 8000


def test_settings_validates_secret_key():
    """Secret key must be secure (min 32 chars, not default)."""
    os.environ["APP_SECRET_KEY"] = "short"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://erp:test@localhost:5432/erp_test"
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    os.environ["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
    os.environ["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
    
    with pytest.raises(Exception):
        Settings()


def test_settings_validates_app_env():
    """app_env must be one of the allowed values."""
    os.environ["APP_SECRET_KEY"] = "test-secret-key-for-testing-minimum-32-chars!!"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://erp:test@localhost:5432/erp_test"
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    os.environ["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
    os.environ["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
    os.environ["APP_ENV"] = "invalid_env"
    
    with pytest.raises(Exception):
        Settings()


def test_settings_validates_pool_size():
    """DB pool size must be within bounds."""
    os.environ["APP_SECRET_KEY"] = "test-secret-key-for-testing-minimum-32-chars!!"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://erp:test@localhost:5432/erp_test"
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    os.environ["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
    os.environ["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
    os.environ["DB_POOL_SIZE"] = "0"
    
    with pytest.raises(Exception):
        Settings()
