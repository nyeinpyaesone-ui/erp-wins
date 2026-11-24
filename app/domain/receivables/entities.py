"""
ERP Platform — Receivables Domain Entities

Receivables represent money owed by customers.
Tracks outstanding balances from sales transactions.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ReceivableStatus(str, Enum):
    """Receivable status."""
    OPEN = "open"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"
    WRITTEN_OFF = "written_off"


class Receivable(BaseModel):
    """
    Receivable entity.
    
    Represents money owed by a customer from a sales transaction.
    """
    id: UUID
    receivable_number: str = Field(min_length=1, max_length=50)  # Unique receivable number
    customer_id: UUID
    sales_order_id: UUID | None = None  # Link to original sales order
    branch_id: UUID
    issue_date: datetime
    due_date: datetime
    total_amount: Decimal = Field(ge=0, decimal_places=2)
    paid_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    outstanding_amount: Decimal = Field(ge=0, decimal_places=2)
    status: ReceivableStatus = ReceivableStatus.OPEN
    notes: str | None = Field(default=None, max_length=2000)
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class ReceivablePayment(BaseModel):
    """
    Receivable payment entity.
    
    Records a payment applied to a receivable.
    """
    id: UUID
    receivable_id: UUID
    payment_id: UUID
    applied_amount: Decimal = Field(gt=0, decimal_places=2)
    applied_date: datetime
    tenant_id: UUID
    created_at: datetime


class ReceivableRepository:
    """Repository interface for Receivable entities."""
    
    async def get_by_id(self, receivable_id: UUID, tenant_id: UUID) -> Receivable | None:
        """Get receivable by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_receivable_number(
        self,
        receivable_number: str,
        tenant_id: UUID,
    ) -> Receivable | None:
        """Get receivable by receivable number within tenant scope."""
        raise NotImplementedError
    
    async def get_by_sales_order(
        self,
        sales_order_id: UUID,
        tenant_id: UUID,
    ) -> Receivable | None:
        """Get receivable by sales order ID."""
        raise NotImplementedError
    
    async def list_by_customer(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Receivable]:
        """List receivables for a customer with pagination."""
        raise NotImplementedError
    
    async def list_overdue(
        self,
        tenant_id: UUID,
        as_of_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Receivable]:
        """List overdue receivables as of a specific date."""
        raise NotImplementedError
    
    async def create(self, receivable: Receivable) -> Receivable:
        """Create a new receivable."""
        raise NotImplementedError
    
    async def update(self, receivable: Receivable) -> Receivable:
        """Update an existing receivable."""
        raise NotImplementedError
    
    async def apply_payment(
        self,
        receivable_id: UUID,
        tenant_id: UUID,
        payment_amount: Decimal,
    ) -> Receivable:
        """Apply a payment to a receivable."""
        raise NotImplementedError


class ReceivablePaymentRepository:
    """Repository interface for ReceivablePayment entities."""
    
    async def create(self, payment: ReceivablePayment) -> ReceivablePayment:
        """Create a receivable payment record."""
        raise NotImplementedError
    
    async def list_by_receivable(
        self,
        receivable_id: UUID,
        tenant_id: UUID,
    ) -> list[ReceivablePayment]:
        """List all payments applied to a receivable."""
        raise NotImplementedError
