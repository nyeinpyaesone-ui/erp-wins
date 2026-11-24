"""
ERP Platform — Sales SQLAlchemy Models

Database implementation of SalesOrder and SalesOrderItem entities.
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class SalesOrderModel(Base):
    """
    SQLAlchemy model for SalesOrder entity.
    
    Table: sales_orders
    """
    __tablename__ = "sales_orders"
    
    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    customer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    branch_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("branches.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False, index=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
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
        return f"<SalesOrder(id={self.id}, order_number={self.order_number}, total={self.total_amount})>"


class SalesOrderItemModel(Base):
    """
    SQLAlchemy model for SalesOrderItem entity.
    
    Table: sales_order_items
    """
    __tablename__ = "sales_order_items"
    
    sales_order_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("sales_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<SalesOrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
