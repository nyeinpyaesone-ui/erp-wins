"""
ERP Platform — Payments Domain Entities

Payments represent financial transactions for settling receivables and payables.
All payment operations are transactional and auditable.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentType(str, Enum):
    """Payment type."""
    CUSTOMER = "customer"  # Payment received from customer
    SUPPLIER = "supplier"  # Payment made to supplier


class PaymentMethod(str, Enum):
    """Payment method."""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CREDIT_CARD = "credit_card"
    MOBILE_PAYMENT = "mobile_payment"
    OTHER = "other"


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Payment(BaseModel):
    """
    Payment entity.
    
    Represents a financial transaction for settling receivables or payables.
    """
    id: UUID
    payment_number: str = Field(min_length=1, max_length=50)  # Unique payment number
    payment_type: PaymentType
    payment_method: PaymentMethod
    party_id: UUID  # customer_id or supplier_id
    branch_id: UUID
    payment_date: datetime
    amount: Decimal = Field(gt=0, decimal_places=2)
    status: PaymentStatus = PaymentStatus.PENDING
    reference_number: str | None = Field(default=None, max_length=100)  # Check number, transaction ID, etc.
    notes: str | None = Field(default=None, max_length=2000)
    created_by: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class PaymentAllocation(BaseModel):
    """
    Payment allocation entity.
    
    Links a payment to specific invoices/orders.
    """
    id: UUID
    payment_id: UUID
    invoice_type: str  # "sales_order" or "purchase_order"
    invoice_id: UUID
    allocated_amount: Decimal = Field(gt=0, decimal_places=2)
    tenant_id: UUID
    created_at: datetime


class PaymentCreate(BaseModel):
    """Data for creating a payment."""
    payment_type: PaymentType
    payment_method: PaymentMethod
    party_id: UUID
    branch_id: UUID
    payment_date: datetime
    amount: Decimal = Field(gt=0, decimal_places=2)
    reference_number: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None, max_length=2000)
    allocations: list[dict]  # List of {invoice_type, invoice_id, allocated_amount}


class PaymentRepository:
    """Repository interface for Payment entities."""
    
    async def get_by_id(self, payment_id: UUID, tenant_id: UUID) -> Payment | None:
        """Get payment by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_payment_number(self, payment_number: str, tenant_id: UUID) -> Payment | None:
        """Get payment by payment number within tenant scope."""
        raise NotImplementedError
    
    async def list_by_party(
        self,
        party_id: UUID,
        payment_type: PaymentType,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        """List payments for a party (customer or supplier) with pagination."""
        raise NotImplementedError
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        """List payments for a branch with pagination."""
        raise NotImplementedError
    
    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        raise NotImplementedError
    
    async def update(self, payment: Payment) -> Payment:
        """Update an existing payment."""
        raise NotImplementedError


class PaymentAllocationRepository:
    """Repository interface for PaymentAllocation entities."""
    
    async def create(self, allocation: PaymentAllocation) -> PaymentAllocation:
        """Create a payment allocation."""
        raise NotImplementedError
    
    async def list_by_payment(self, payment_id: UUID, tenant_id: UUID) -> list[PaymentAllocation]:
        """List all allocations for a payment."""
        raise NotImplementedError
    
    async def list_by_invoice(
        self,
        invoice_type: str,
        invoice_id: UUID,
        tenant_id: UUID,
    ) -> list[PaymentAllocation]:
        """List all allocations for an invoice."""
        raise NotImplementedError
