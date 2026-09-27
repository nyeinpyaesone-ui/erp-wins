"""
ERP Platform — Sales Repository Implementation

SQLAlchemy implementation of SalesOrderRepository interface.
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sales.entities import (
    SalesOrder,
    SalesOrderItem,
    SalesOrderRepository,
    SalesOrderItemRepository,
)
from app.infrastructure.database.models.sales import SalesOrderModel, SalesOrderItemModel


class SQLAlchemySalesOrderRepository(SalesOrderRepository):
    """SQLAlchemy implementation of SalesOrderRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: SalesOrderModel) -> SalesOrder:
        """Convert SQLAlchemy model to domain entity."""
        return SalesOrder(
            id=model.id,
            order_number=model.order_number,
            customer_id=model.customer_id,
            branch_id=model.branch_id,
            order_date=model.order_date,
            status=model.status,
            subtotal=model.subtotal,
            tax_amount=model.tax_amount,
            discount_amount=model.discount_amount,
            total_amount=model.total_amount,
            paid_amount=model.paid_amount,
            payment_status=model.payment_status,
            notes=model.notes,
            created_by=model.created_by,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, order: SalesOrder) -> SalesOrderModel:
        """Convert domain entity to SQLAlchemy model."""
        return SalesOrderModel(
            id=order.id,
            order_number=order.order_number,
            customer_id=order.customer_id,
            branch_id=order.branch_id,
            order_date=order.order_date,
            status=order.status,
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            discount_amount=order.discount_amount,
            total_amount=order.total_amount,
            paid_amount=order.paid_amount,
            payment_status=order.payment_status,
            notes=order.notes,
            created_by=order.created_by,
            tenant_id=order.tenant_id,
        )
    
    async def get_by_id(self, order_id: UUID, tenant_id: UUID) -> SalesOrder | None:
        """Get sales order by ID within tenant scope."""
        result = await self.session.execute(
            select(SalesOrderModel).where(
                SalesOrderModel.id == order_id,
                SalesOrderModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_order_number(self, order_number: str, tenant_id: UUID) -> SalesOrder | None:
        """Get sales order by order number within tenant scope."""
        result = await self.session.execute(
            select(SalesOrderModel).where(
                SalesOrderModel.order_number == order_number,
                SalesOrderModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def list_by_customer(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        """List sales orders for a customer with pagination."""
        result = await self.session.execute(
            select(SalesOrderModel)
            .where(
                SalesOrderModel.customer_id == customer_id,
                SalesOrderModel.tenant_id == tenant_id,
            )
            .order_by(SalesOrderModel.order_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SalesOrder]:
        """List sales orders for a branch with pagination."""
        result = await self.session.execute(
            select(SalesOrderModel)
            .where(
                SalesOrderModel.branch_id == branch_id,
                SalesOrderModel.tenant_id == tenant_id,
            )
            .order_by(SalesOrderModel.order_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def create(self, order: SalesOrder) -> SalesOrder:
        """Create a new sales order."""
        model = self._to_model(order)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, order: SalesOrder) -> SalesOrder:
        """Update an existing sales order."""
        result = await self.session.execute(
            select(SalesOrderModel).where(
                SalesOrderModel.id == order.id,
                SalesOrderModel.tenant_id == order.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"SalesOrder {order.id} not found")
        
        # Update fields
        model.status = order.status
        model.subtotal = order.subtotal
        model.tax_amount = order.tax_amount
        model.discount_amount = order.discount_amount
        model.total_amount = order.total_amount
        model.paid_amount = order.paid_amount
        model.payment_status = order.payment_status
        model.notes = order.notes
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update_payment(
        self,
        order_id: UUID,
        tenant_id: UUID,
        paid_amount: Decimal,
    ) -> SalesOrder:
        """Update payment status and amount."""
        result = await self.session.execute(
            select(SalesOrderModel).where(
                SalesOrderModel.id == order_id,
                SalesOrderModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"SalesOrder {order_id} not found")
        
        model.paid_amount = paid_amount
        
        # Update payment status
        if paid_amount >= model.total_amount:
            model.payment_status = "paid"
        elif paid_amount > 0:
            model.payment_status = "partial"
        else:
            model.payment_status = "pending"
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)


class SQLAlchemySalesOrderItemRepository(SalesOrderItemRepository):
    """SQLAlchemy implementation of SalesOrderItemRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: SalesOrderItemModel) -> SalesOrderItem:
        """Convert SQLAlchemy model to domain entity."""
        return SalesOrderItem(
            id=model.id,
            sales_order_id=model.sales_order_id,
            product_id=model.product_id,
            quantity=model.quantity,
            unit_price=model.unit_price,
            discount_amount=model.discount_amount,
            line_total=model.line_total,
            notes=model.notes,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
        )
    
    def _to_model(self, item: SalesOrderItem) -> SalesOrderItemModel:
        """Convert domain entity to SQLAlchemy model."""
        return SalesOrderItemModel(
            id=item.id,
            sales_order_id=item.sales_order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_amount=item.discount_amount,
            line_total=item.line_total,
            notes=item.notes,
            tenant_id=item.tenant_id,
        )
    
    async def create(self, item: SalesOrderItem) -> SalesOrderItem:
        """Create a sales order item."""
        model = self._to_model(item)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def list_by_order(self, order_id: UUID, tenant_id: UUID) -> list[SalesOrderItem]:
        """List all items for a sales order."""
        result = await self.session.execute(
            select(SalesOrderItemModel).where(
                SalesOrderItemModel.sales_order_id == order_id,
                SalesOrderItemModel.tenant_id == tenant_id,
            )
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def delete_by_order(self, order_id: UUID, tenant_id: UUID) -> bool:
        """Delete all items for a sales order."""
        result = await self.session.execute(
            select(SalesOrderItemModel).where(
                SalesOrderItemModel.sales_order_id == order_id,
                SalesOrderItemModel.tenant_id == tenant_id,
            )
        )
        items = result.scalars().all()
        for item in items:
            await self.session.delete(item)
        await self.session.flush()
        return len(items) > 0
