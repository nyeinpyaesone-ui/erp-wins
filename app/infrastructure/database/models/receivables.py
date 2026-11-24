"""
ERP Platform — Receivables SQLAlchemy Models

Database implementation of Receivable and ReceivablePayment entities.
"""

from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ReceivableModel(Base):
    """
    SQLAlchemy model for Receivable entity.
    
    Table: receivables
    """
    __tablename__ = "receivables"
    
    receivable_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    customer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sales_order_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("sales_orders.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    branch_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("branches.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    issue_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    outstanding_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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
        return f"<Receivable(id={self.id}, receivable_number={self.receivable_number}, outstanding={self.outstanding_amount})>"


class ReceivablePaymentModel(Base):
    """
    SQLAlchemy model for ReceivablePayment entity.
    
    Table: receivable_payments
    """
    __tablename__ = "receivable_payments"
    
    receivable_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("receivables.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    payment_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("payments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    applied_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    applied_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<ReceivablePayment(id={self.id}, receivable_id={self.receivable_id}, amount={self.applied_amount})>"
