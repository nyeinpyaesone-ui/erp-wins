"""
ERP Platform — Payables Domain Entities

Payables represent money owed to suppliers.
Tracks outstanding balances from purchase transactions.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PayableStatus(str, Enum):
    """Payable status."""
    OPEN = "open"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"
    WRITTEN_OFF = "written_off"


class Payable(BaseModel):
    """
    Payable entity.
    
    Represents money owed to a supplier from a purchase transaction.
    """
    id: UUID
    payable_number: str = Field(min_length=1, max_length=50)  # Unique payable number
    supplier_id: UUID
    purchase_order_id: UUID | None = None  # Link to original purchase order
    branch_id: UUID
    issue_date: datetime
    due_date: datetime
    total_amount: Decimal = Field(ge=0, decimal_places=2)
    paid_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    outstanding_amount: Decimal = Field(ge=0, decimal_places=2)
    status: PayableStatus = PayableStatus.OPEN
    notes: str | None = Field(default=None, max_length=2000)
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class PayablePayment(BaseModel):
    """
    Payable payment entity.
    
    Records a payment made against a payable.
    """
    id: UUID
    payable_id: UUID
    payment_id: UUID
    applied_amount: Decimal = Field(gt=0, decimal_places=2)
    applied_date: datetime
    tenant_id: UUID
    created_at: datetime


class PayableRepository:
    """Repository interface for Payable entities."""
    
    async def get_by_id(self, payable_id: UUID, tenant_id: UUID) -> Payable | None:
        """Get payable by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_payable_number(
        self,
        payable_number: str,
        tenant_id: UUID,
    ) -> Payable | None:
        """Get payable by payable number within tenant scope."""
        raise NotImplementedError
    
    async def get_by_purchase_order(
        self,
        purchase_order_id: UUID,
        tenant_id: UUID,
    ) -> Payable | None:
        """Get payable by purchase order ID."""
        raise NotImplementedError
    
    async def list_by_supplier(
        self,
        supplier_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payable]:
        """List payables for a supplier with pagination."""
        raise NotImplementedError
    
    async def list_overdue(
        self,
        tenant_id: UUID,
        as_of_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payable]:
        """List overdue payables as of a specific date."""
        raise NotImplementedError
    
    async def create(self, payable: Payable) -> Payable:
        """Create a new payable."""
        raise NotImplementedError
    
    async def update(self, payable: Payable) -> Payable:
        """Update an existing payable."""
        raise NotImplementedError
    
    async def apply_payment(
        self,
        payable_id: UUID,
        tenant_id: UUID,
        payment_amount: Decimal,
    ) -> Payable:
        """Apply a payment to a payable."""
        raise NotImplementedError


class PayablePaymentRepository:
    """Repository interface for PayablePayment entities."""
    
    async def create(self, payment: PayablePayment) -> PayablePayment:
        """Create a payable payment record."""
        raise NotImplementedError
    
    async def list_by_payable(
        self,
        payable_id: UUID,
        tenant_id: UUID,
    ) -> list[PayablePayment]:
        """List all payments applied to a payable."""
        raise NotImplementedError
