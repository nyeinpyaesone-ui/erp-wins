"""
ERP Platform — Sales Application Service

Orchestrates sales order business logic.
"""

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.sales.entities import (
    SalesOrder,
    SalesOrderItem,
    SalesOrderCreate,
    SalesOrderRepository,
    SalesOrderItemRepository,
    SalesOrderStatus,
)
from app.domain.exceptions import EntityNotFoundException, ValidationException


class SalesService:
    """Application service for sales operations."""
    
    def __init__(
        self,
        order_repository: SalesOrderRepository,
        item_repository: SalesOrderItemRepository,
    ):
        self.order_repository = order_repository
        self.item_repository = item_repository
    
    async def create_sales_order(
        self,
        data: SalesOrderCreate,
        created_by: UUID,
        tenant_id: UUID,
    ) -> SalesOrder:
        """
        Create a new sales order with items.
        
        Business rules:
        - Calculate totals from line items
        - Generate unique order number
        - Set initial status to DRAFT
        """
        # Generate order number
        order_number = f"SO-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid4().hex[:8].upper()}"
        
        # Calculate totals from items
        subtotal = Decimal("0")
        items_to_create = []
        
        for item_data in data.items:
            quantity = Decimal(str(item_data["quantity"]))
            unit_price = Decimal(str(item_data["unit_price"]))
            discount = Decimal(str(item_data.get("discount_amount", "0")))
            
            line_total = (quantity * unit_price) - discount
            subtotal += line_total
            
            item = SalesOrderItem(
                id=uuid4(),
                sales_order_id=UUID(int=0),  # Will be updated after order creation
                product_id=UUID(item_data["product_id"]),
                quantity=quantity,
                unit_price=unit_price,
                discount_amount=discount,
                line_total=line_total,
                notes=item_data.get("notes"),
                tenant_id=tenant_id,
                created_at=datetime.now(timezone.utc),
            )
            items_to_create.append(item)
        
        total_amount = subtotal + data.tax_amount - data.discount_amount
        
        # Create order
        order = SalesOrder(
            id=uuid4(),
            order_number=order_number,
            customer_id=data.customer_id,
            branch_id=data.branch_id,
            order_date=data.order_date,
            status=SalesOrderStatus.DRAFT,
            subtotal=subtotal,
            tax_amount=data.tax_amount,
            discount_amount=data.discount_amount,
            total_amount=total_amount,
            paid_amount=Decimal("0"),
            payment_status="pending",
            notes=data.notes,
            created_by=created_by,
            tenant_id=tenant_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        
        created_order = await self.order_repository.create(order)
        
        # Create items with correct order ID
        for item in items_to_create:
            item.sales_order_id = created_order.id
            await self.item_repository.create(item)
        
        return created_order
    
    async def confirm_order(
        self,
        order_id: UUID,
        tenant_id: UUID,
    ) -> SalesOrder:
        """
        Confirm a draft sales order.
        
        Business rules:
        - Order must be in DRAFT status
        - Transitions to CONFIRMED status
        """
        order = await self.order_repository.get_by_id(order_id, tenant_id)
        if not order:
            raise EntityNotFoundException("SalesOrder", order_id)
        
        if order.status != SalesOrderStatus.DRAFT:
            raise ValidationException(
                f"Cannot confirm order in {order.status} status",
                field="status",
            )
        
        order.status = SalesOrderStatus.CONFIRMED
        return await self.order_repository.update(order)
    
    async def complete_order(
        self,
        order_id: UUID,
        tenant_id: UUID,
    ) -> SalesOrder:
        """
        Complete a sales order.
        
        Business rules:
        - Order must be in PROCESSING status
        - Transitions to COMPLETED status
        """
        order = await self.order_repository.get_by_id(order_id, tenant_id)
        if not order:
            raise EntityNotFoundException("SalesOrder", order_id)
        
        if order.status != SalesOrderStatus.PROCESSING:
            raise ValidationException(
                f"Cannot complete order in {order.status} status",
                field="status",
            )
        
        order.status = SalesOrderStatus.COMPLETED
        return await self.order_repository.update(order)
    
    async def get_order(self, order_id: UUID, tenant_id: UUID) -> SalesOrder:
        """Get a sales order by ID."""
        order = await self.order_repository.get_by_id(order_id, tenant_id)
        if not order:
            raise EntityNotFoundException("SalesOrder", order_id)
        return order
    
    async def get_order_items(
        self,
        order_id: UUID,
        tenant_id: UUID,
    ) -> list[SalesOrderItem]:
        """Get all items for a sales order."""
        return await self.item_repository.list_by_order(order_id, tenant_id)
    
    async def list_orders_by_customer(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        """List sales orders for a customer."""
        return await self.order_repository.list_by_customer(
            customer_id, tenant_id, skip, limit
        )
    
    async def list_orders_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        """List sales orders for a branch."""
        return await self.order_repository.list_by_branch(
            branch_id, tenant_id, skip, limit
        )
