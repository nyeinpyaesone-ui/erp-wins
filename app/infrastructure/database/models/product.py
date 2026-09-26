"""
ERP Platform — Product SQLAlchemy Model

Database implementation of Product entity.
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ProductModel(Base):
    """
    SQLAlchemy model for Product entity.
    
    Table: products
    """
    __tablename__ = "products"
    
    sku: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    type: Mapped[str] = mapped_column(String(20), default="physical", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    category_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    unit_of_measure: Mapped[str] = mapped_column(String(20), default="piece", nullable=False)
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    is_trackable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    
    # Timestamps
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
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, sku={self.sku}, name={self.name})>"
