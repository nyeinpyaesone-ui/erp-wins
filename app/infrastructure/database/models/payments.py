"""
ERP Platform — Payments SQLAlchemy Models

Database implementation of Payment and PaymentAllocation entities.
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class PaymentModel(Base):
    """
    SQLAlchemy model for Payment entity.
    
    Table: payments
    """
    __tablename__ = "payments"
    
    payment_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    payment_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # "customer" or "supplier"
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)
    party_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    branch_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("branches.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
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
        return f"<Payment(id={self.id}, payment_number={self.payment_number}, amount={self.amount})>"


class PaymentAllocationModel(Base):
    """
    SQLAlchemy model for PaymentAllocation entity.
    
    Table: payment_allocations
    """
    __tablename__ = "payment_allocations"
    
    payment_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    invoice_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # "sales_order" or "purchase_order"
    invoice_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<PaymentAllocation(id={self.id}, payment_id={self.payment_id}, amount={self.allocated_amount})>"
