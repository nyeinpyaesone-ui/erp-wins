"""
ERP Platform — Daily Closing SQLAlchemy Model

Database implementation of DailyClosing entity.
"""

from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DailyClosingModel(Base):
    """
    SQLAlchemy model for DailyClosing entity.
    
    Table: daily_closings
    """
    __tablename__ = "daily_closings"
    
    closing_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    branch_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("branches.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    closing_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False, index=True)
    
    # Sales summary
    total_sales: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    sales_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Purchase summary
    total_purchases: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    purchase_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Payment summary
    total_customer_payments: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    customer_payment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_supplier_payments: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    supplier_payment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Cash summary
    opening_cash: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    closing_cash: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    expected_cash: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    cash_difference: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"), nullable=False)
    
    # Notes and approval
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    approved_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
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
        return f"<DailyClosing(id={self.id}, closing_number={self.closing_number}, date={self.closing_date})>"
