"""
ERP Platform — Celery Application

Celery handles asynchronous work.
Tasks must be idempotent, retry-safe, time-bounded, observable, and failure-aware.
"""

from celery import Celery

from app.config import get_settings


def create_celery_app() -> Celery:
    """Create and configure the Celery application."""
    settings = get_settings()
    
    app = Celery(
        "erp",
        broker=str(settings.celery_broker_url),
        backend=str(settings.celery_result_backend),
    )
    
    # Configuration
    app.conf.update(
        # Serialization
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        
        # Timezone
        timezone="UTC",
        enable_utc=True,
        
        # Task execution
        task_acks_late=True,  # Acknowledge after execution
        task_reject_on_worker_lost=True,
        worker_prefetch_multiplier=1,  # Fair dispatch
        
        # Retry
        task_default_retry_delay=60,
        task_max_retries=3,
        
        # Result backend
        result_expires=3600,  # 1 hour
        
        # Beat schedule (periodic tasks)
        beat_schedule={},
    )
    
    # Auto-discover tasks
    app.autodiscover_tasks(["workers.tasks"])
    
    return app


# Global Celery app instance
celery_app = create_celery_app()
