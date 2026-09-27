"""
ERP Platform — Purchases Domain Entities

Purchase orders represent supplier transactions.
All purchase operations are transactional and auditable.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PurchaseOrderStatus(str, Enum):
    """Purchase order status."""
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    RECEIVED = "received"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERPAID = "overpaid"


class PurchaseOrder(BaseModel):
    """
    Purchase order entity.
    
    Represents a supplier purchase transaction.
    """
    id: UUID
    order_number: str = Field(min_length=1, max_length=50)  # Unique order number
    supplier_id: UUID
    branch_id: UUID
    order_date: datetime
    status: PurchaseOrderStatus = PurchaseOrderStatus.DRAFT
    subtotal: Decimal = Field(ge=0, decimal_places=2)
    tax_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    total_amount: Decimal = Field(ge=0, decimal_places=2)
    paid_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    payment_status: PaymentStatus = PaymentStatus.PENDING
    notes: str | None = Field(default=None, max_length=2000)
    created_by: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class PurchaseOrderItem(BaseModel):
    """
    Purchase order item entity.
    
    Represents a line item in a purchase order.
    """
    id: UUID
    purchase_order_id: UUID
    product_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)
    unit_price: Decimal = Field(ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    line_total: Decimal = Field(ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=500)
    tenant_id: UUID
    created_at: datetime


class PurchaseOrderCreate(BaseModel):
    """Data for creating a purchase order."""
    supplier_id: UUID
    branch_id: UUID
    order_date: datetime
    items: list[dict]  # List of {product_id, quantity, unit_price, discount_amount}
    tax_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class PurchaseOrderUpdate(BaseModel):
    """Data for updating a purchase order."""
    status: PurchaseOrderStatus | None = None
    notes: str | None = Field(default=None, max_length=2000)


class PurchaseOrderRepository:
    """Repository interface for PurchaseOrder entities."""
    
    async def get_by_id(self, order_id: UUID, tenant_id: UUID) -> PurchaseOrder | None:
        """Get purchase order by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_order_number(self, order_number: str, tenant_id: UUID) -> PurchaseOrder | None:
        """Get purchase order by order number within tenant scope."""
        raise NotImplementedError
    
    async def list_by_supplier(
        self,
        supplier_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[PurchaseOrder]:
        """List purchase orders for a supplier with pagination."""
        raise NotImplementedError
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[PurchaseOrder]:
        """List purchase orders for a branch with pagination."""
        raise NotImplementedError
    
    async def create(self, order: PurchaseOrder) -> PurchaseOrder:
        """Create a new purchase order."""
        raise NotImplementedError
    
    async def update(self, order: PurchaseOrder) -> PurchaseOrder:
        """Update an existing purchase order."""
        raise NotImplementedError
    
    async def update_payment(
        self,
        order_id: UUID,
        tenant_id: UUID,
        paid_amount: Decimal,
    ) -> PurchaseOrder:
        """Update payment status and amount."""
        raise NotImplementedError


class PurchaseOrderItemRepository:
    """Repository interface for PurchaseOrderItem entities."""
    
    async def create(self, item: PurchaseOrderItem) -> PurchaseOrderItem:
        """Create a purchase order item."""
        raise NotImplementedError
    
    async def list_by_order(self, order_id: UUID, tenant_id: UUID) -> list[PurchaseOrderItem]:
        """List all items for a purchase order."""
        raise NotImplementedError
    
    async def delete_by_order(self, order_id: UUID, tenant_id: UUID) -> bool:
        """Delete all items for a purchase order."""
        raise NotImplementedError
