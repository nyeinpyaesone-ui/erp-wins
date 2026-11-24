"""
ERP Platform — SQLAlchemy Base Model

All domain models inherit from this base.
Uses timezone-aware timestamps.
"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""
    pass


class TimestampMixin:
    """Mixin for timezone-aware created/updated timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """Mixin for UUID primary keys."""

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )


class TenantMixin:
    """Mixin for multi-tenant isolation."""

    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )


class BaseModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Base model with UUID primary key and timestamps.
    
    All domain entities should inherit from this.
    """
    pass
