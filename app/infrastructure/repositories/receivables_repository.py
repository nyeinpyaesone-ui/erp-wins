"""
ERP Platform — Receivables Repository Implementation
"""

from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.receivables.entities import (
    Receivable,
    ReceivablePayment,
    ReceivableRepository,
    ReceivablePaymentRepository,
)
from app.infrastructure.database.models.receivables import ReceivableModel, ReceivablePaymentModel


class SQLAlchemyReceivableRepository(ReceivableRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: ReceivableModel) -> Receivable:
        return Receivable(
            id=model.id,
            receivable_number=model.receivable_number,
            customer_id=model.customer_id,
            sales_order_id=model.sales_order_id,
            branch_id=model.branch_id,
            issue_date=model.issue_date,
            due_date=model.due_date,
            total_amount=model.total_amount,
            paid_amount=model.paid_amount,
            outstanding_amount=model.outstanding_amount,
            status=model.status,
            notes=model.notes,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, receivable: Receivable) -> ReceivableModel:
        return ReceivableModel(
            id=receivable.id,
            receivable_number=receivable.receivable_number,
            customer_id=receivable.customer_id,
            sales_order_id=receivable.sales_order_id,
            branch_id=receivable.branch_id,
            issue_date=receivable.issue_date,
            due_date=receivable.due_date,
            total_amount=receivable.total_amount,
            paid_amount=receivable.paid_amount,
            outstanding_amount=receivable.outstanding_amount,
            status=receivable.status,
            notes=receivable.notes,
            tenant_id=receivable.tenant_id,
        )
    
    async def get_by_id(self, receivable_id: UUID, tenant_id: UUID) -> Receivable | None:
        result = await self.session.execute(
            select(ReceivableModel).where(
                ReceivableModel.id == receivable_id,
                ReceivableModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_receivable_number(self, receivable_number: str, tenant_id: UUID) -> Receivable | None:
        result = await self.session.execute(
            select(ReceivableModel).where(
                ReceivableModel.receivable_number == receivable_number,
                ReceivableModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_sales_order(self, sales_order_id: UUID, tenant_id: UUID) -> Receivable | None:
        result = await self.session.execute(
            select(ReceivableModel).where(
                ReceivableModel.sales_order_id == sales_order_id,
                ReceivableModel.tenant_id == tenant_id,
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
    ) -> list[Receivable]:
        result = await self.session.execute(
            select(ReceivableModel)
            .where(
                ReceivableModel.customer_id == customer_id,
                ReceivableModel.tenant_id == tenant_id,
            )
            .order_by(ReceivableModel.issue_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def list_overdue(
        self,
        tenant_id: UUID,
        as_of_date: date,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Receivable]:
        result = await self.session.execute(
            select(ReceivableModel)
            .where(
                ReceivableModel.tenant_id == tenant_id,
                ReceivableModel.due_date < as_of_date,
                ReceivableModel.status.in_(["open", "partial"]),
            )
            .order_by(ReceivableModel.due_date.asc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def create(self, receivable: Receivable) -> Receivable:
        model = self._to_model(receivable)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, receivable: Receivable) -> Receivable:
        result = await self.session.execute(
            select(ReceivableModel).where(
                ReceivableModel.id == receivable.id,
                ReceivableModel.tenant_id == receivable.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Receivable {receivable.id} not found")
        
        model.paid_amount = receivable.paid_amount
        model.outstanding_amount = receivable.outstanding_amount
        model.status = receivable.status
        model.notes = receivable.notes
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def apply_payment(
        self,
        receivable_id: UUID,
        tenant_id: UUID,
        payment_amount: Decimal,
    ) -> Receivable:
        result = await self.session.execute(
            select(ReceivableModel).where(
                ReceivableModel.id == receivable_id,
                ReceivableModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Receivable {receivable_id} not found")
        
        model.paid_amount += payment_amount
        model.outstanding_amount = model.total_amount - model.paid_amount
        
        if model.outstanding_amount <= 0:
            model.status = "paid"
        elif model.paid_amount > 0:
            model.status = "partial"
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)


class SQLAlchemyReceivablePaymentRepository(ReceivablePaymentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: ReceivablePaymentModel) -> ReceivablePayment:
        return ReceivablePayment(
            id=model.id,
            receivable_id=model.receivable_id,
            payment_id=model.payment_id,
            applied_amount=model.applied_amount,
            applied_date=model.applied_date,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
        )
    
    def _to_model(self, payment: ReceivablePayment) -> ReceivablePaymentModel:
        return ReceivablePaymentModel(
            id=payment.id,
            receivable_id=payment.receivable_id,
            payment_id=payment.payment_id,
            applied_amount=payment.applied_amount,
            applied_date=payment.applied_date,
            tenant_id=payment.tenant_id,
        )
    
    async def create(self, payment: ReceivablePayment) -> ReceivablePayment:
        model = self._to_model(payment)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def list_by_receivable(
        self,
        receivable_id: UUID,
        tenant_id: UUID,
    ) -> list[ReceivablePayment]:
        result = await self.session.execute(
            select(ReceivablePaymentModel).where(
                ReceivablePaymentModel.receivable_id == receivable_id,
                ReceivablePaymentModel.tenant_id == tenant_id,
            )
        )
        return [self._to_domain(model) for model in result.scalars().all()]
