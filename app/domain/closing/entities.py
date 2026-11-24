"""
ERP Platform — Daily Closing Domain Entities

Daily closing represents end-of-day financial reconciliation.
Ensures all transactions are properly recorded and balanced.
"""

from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ClosingStatus(str, Enum):
    """Closing status."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    REJECTED = "rejected"


class DailyClosing(BaseModel):
    """
    Daily closing entity.
    
    Represents end-of-day financial reconciliation for a branch.
    """
    id: UUID
    closing_number: str = Field(min_length=1, max_length=50)  # Unique closing number
    branch_id: UUID
    closing_date: date
    status: ClosingStatus = ClosingStatus.DRAFT
    
    # Sales summary
    total_sales: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    sales_count: int = Field(default=0, ge=0)
    
    # Purchase summary
    total_purchases: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    purchase_count: int = Field(default=0, ge=0)
    
    # Payment summary
    total_customer_payments: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    customer_payment_count: int = Field(default=0, ge=0)
    total_supplier_payments: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    supplier_payment_count: int = Field(default=0, ge=0)
    
    # Cash summary
    opening_cash: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    closing_cash: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    expected_cash: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    cash_difference: Decimal = Field(default=Decimal("0"), decimal_places=2)
    
    # Notes and approval
    notes: str | None = Field(default=None, max_length=2000)
    created_by: UUID
    approved_by: UUID | None = None
    approved_at: datetime | None = None
    
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class DailyClosingCreate(BaseModel):
    """Data for creating a daily closing."""
    branch_id: UUID
    closing_date: date
    opening_cash: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class DailyClosingUpdate(BaseModel):
    """Data for updating a daily closing."""
    closing_cash: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)
    status: ClosingStatus | None = None


class DailyClosingRepository:
    """Repository interface for DailyClosing entities."""
    
    async def get_by_id(self, closing_id: UUID, tenant_id: UUID) -> DailyClosing | None:
        """Get daily closing by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_closing_number(
        self,
        closing_number: str,
        tenant_id: UUID,
    ) -> DailyClosing | None:
        """Get daily closing by closing number within tenant scope."""
        raise NotImplementedError
    
    async def get_by_branch_and_date(
        self,
        branch_id: UUID,
        closing_date: date,
        tenant_id: UUID,
    ) -> DailyClosing | None:
        """Get daily closing by branch and date."""
        raise NotImplementedError
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DailyClosing]:
        """List daily closings for a branch with pagination."""
        raise NotImplementedError
    
    async def create(self, closing: DailyClosing) -> DailyClosing:
        """Create a new daily closing."""
        raise NotImplementedError
    
    async def update(self, closing: DailyClosing) -> DailyClosing:
        """Update an existing daily closing."""
        raise NotImplementedError
    
    async def approve(
        self,
        closing_id: UUID,
        tenant_id: UUID,
        approved_by: UUID,
    ) -> DailyClosing:
        """Approve a daily closing."""
        raise NotImplementedError
