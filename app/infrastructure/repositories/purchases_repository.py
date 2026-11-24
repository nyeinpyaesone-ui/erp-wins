"""
ERP Platform — Purchases Repository Implementation
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.purchases.entities import (
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseOrderRepository,
    PurchaseOrderItemRepository,
)
from app.infrastructure.database.models.purchases import PurchaseOrderModel, PurchaseOrderItemModel


class SQLAlchemyPurchaseOrderRepository(PurchaseOrderRepository):
    """SQLAlchemy implementation of PurchaseOrderRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: PurchaseOrderModel) -> PurchaseOrder:
        return PurchaseOrder(
            id=model.id,
            order_number=model.order_number,
            supplier_id=model.supplier_id,
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
    
    def _to_model(self, order: PurchaseOrder) -> PurchaseOrderModel:
        return PurchaseOrderModel(
            id=order.id,
            order_number=order.order_number,
            supplier_id=order.supplier_id,
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
    
    async def get_by_id(self, order_id: UUID, tenant_id: UUID) -> PurchaseOrder | None:
        result = await self.session.execute(
            select(PurchaseOrderModel).where(
                PurchaseOrderModel.id == order_id,
                PurchaseOrderModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_order_number(self, order_number: str, tenant_id: UUID) -> PurchaseOrder | None:
        result = await self.session.execute(
            select(PurchaseOrderModel).where(
                PurchaseOrderModel.order_number == order_number,
                PurchaseOrderModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def list_by_supplier(
        self,
        supplier_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[PurchaseOrder]:
        result = await self.session.execute(
            select(PurchaseOrderModel)
            .where(
                PurchaseOrderModel.supplier_id == supplier_id,
                PurchaseOrderModel.tenant_id == tenant_id,
            )
            .order_by(PurchaseOrderModel.order_date.desc())
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
    ) -> list[PurchaseOrder]:
        result = await self.session.execute(
            select(PurchaseOrderModel)
            .where(
                PurchaseOrderModel.branch_id == branch_id,
                PurchaseOrderModel.tenant_id == tenant_id,
            )
            .order_by(PurchaseOrderModel.order_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def create(self, order: PurchaseOrder) -> PurchaseOrder:
        model = self._to_model(order)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, order: PurchaseOrder) -> PurchaseOrder:
        result = await self.session.execute(
            select(PurchaseOrderModel).where(
                PurchaseOrderModel.id == order.id,
                PurchaseOrderModel.tenant_id == order.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"PurchaseOrder {order.id} not found")
        
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
    ) -> PurchaseOrder:
        result = await self.session.execute(
            select(PurchaseOrderModel).where(
                PurchaseOrderModel.id == order_id,
                PurchaseOrderModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"PurchaseOrder {order_id} not found")
        
        model.paid_amount = paid_amount
        
        if paid_amount >= model.total_amount:
            model.payment_status = "paid"
        elif paid_amount > 0:
            model.payment_status = "partial"
        else:
            model.payment_status = "pending"
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)


class SQLAlchemyPurchaseOrderItemRepository(PurchaseOrderItemRepository):
    """SQLAlchemy implementation of PurchaseOrderItemRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: PurchaseOrderItemModel) -> PurchaseOrderItem:
        return PurchaseOrderItem(
            id=model.id,
            purchase_order_id=model.purchase_order_id,
            product_id=model.product_id,
            quantity=model.quantity,
            unit_price=model.unit_price,
            discount_amount=model.discount_amount,
            line_total=model.line_total,
            notes=model.notes,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
        )
    
    def _to_model(self, item: PurchaseOrderItem) -> PurchaseOrderItemModel:
        return PurchaseOrderItemModel(
            id=item.id,
            purchase_order_id=item.purchase_order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_amount=item.discount_amount,
            line_total=item.line_total,
            notes=item.notes,
            tenant_id=item.tenant_id,
        )
    
    async def create(self, item: PurchaseOrderItem) -> PurchaseOrderItem:
        model = self._to_model(item)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def list_by_order(self, order_id: UUID, tenant_id: UUID) -> list[PurchaseOrderItem]:
        result = await self.session.execute(
            select(PurchaseOrderItemModel).where(
                PurchaseOrderItemModel.purchase_order_id == order_id,
                PurchaseOrderItemModel.tenant_id == tenant_id,
            )
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def delete_by_order(self, order_id: UUID, tenant_id: UUID) -> bool:
        result = await self.session.execute(
            select(PurchaseOrderItemModel).where(
                PurchaseOrderItemModel.purchase_order_id == order_id,
                PurchaseOrderItemModel.tenant_id == tenant_id,
            )
        )
        items = result.scalars().all()
        for item in items:
            await self.session.delete(item)
        await self.session.flush()
        return len(items) > 0
