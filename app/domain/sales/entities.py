"""
ERP Platform — Sales Domain Entities

Sales orders represent customer transactions.
All sales operations are transactional and auditable.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class SalesOrderStatus(str, Enum):
    """Sales order status."""
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERPAID = "overpaid"


class SalesOrder(BaseModel):
    """
    Sales order entity.
    
    Represents a customer sales transaction.
    """
    id: UUID
    order_number: str = Field(min_length=1, max_length=50)  # Unique order number
    customer_id: UUID
    branch_id: UUID
    order_date: datetime
    status: SalesOrderStatus = SalesOrderStatus.DRAFT
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


class SalesOrderItem(BaseModel):
    """
    Sales order item entity.
    
    Represents a line item in a sales order.
    """
    id: UUID
    sales_order_id: UUID
    product_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)
    unit_price: Decimal = Field(ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    line_total: Decimal = Field(ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=500)
    tenant_id: UUID
    created_at: datetime


class SalesOrderCreate(BaseModel):
    """Data for creating a sales order."""
    customer_id: UUID
    branch_id: UUID
    order_date: datetime
    items: list[dict]  # List of {product_id, quantity, unit_price, discount_amount}
    tax_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class SalesOrderUpdate(BaseModel):
    """Data for updating a sales order."""
    status: SalesOrderStatus | None = None
    notes: str | None = Field(default=None, max_length=2000)


class SalesOrderRepository:
    """Repository interface for SalesOrder entities."""
    
    async def get_by_id(self, order_id: UUID, tenant_id: UUID) -> SalesOrder | None:
        """Get sales order by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_order_number(self, order_number: str, tenant_id: UUID) -> SalesOrder | None:
        """Get sales order by order number within tenant scope."""
        raise NotImplementedError
    
    async def list_by_customer(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        """List sales orders for a customer with pagination."""
        raise NotImplementedError
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        """List sales orders for a branch with pagination."""
        raise NotImplementedError
    
    async def create(self, order: SalesOrder) -> SalesOrder:
        """Create a new sales order."""
        raise NotImplementedError
    
    async def update(self, order: SalesOrder) -> SalesOrder:
        """Update an existing sales order."""
        raise NotImplementedError
    
    async def update_payment(
        self,
        order_id: UUID,
        tenant_id: UUID,
        paid_amount: Decimal,
    ) -> SalesOrder:
        """Update payment status and amount."""
        raise NotImplementedError


class SalesOrderItemRepository:
    """Repository interface for SalesOrderItem entities."""
    
    async def create(self, item: SalesOrderItem) -> SalesOrderItem:
        """Create a sales order item."""
        raise NotImplementedError
    
    async def list_by_order(self, order_id: UUID, tenant_id: UUID) -> list[SalesOrderItem]:
        """List all items for a sales order."""
        raise NotImplementedError
    
    async def delete_by_order(self, order_id: UUID, tenant_id: UUID) -> bool:
        """Delete all items for a sales order."""
        raise NotImplementedError
