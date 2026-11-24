"""
ERP Platform — Payables Repository Implementation
"""

from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.payables.entities import (
    Payable,
    PayablePayment,
    PayableRepository,
    PayablePaymentRepository,
)
from app.infrastructure.database.models.payables import PayableModel, PayablePaymentModel


class SQLAlchemyPayableRepository(PayableRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: PayableModel) -> Payable:
        return Payable(
            id=model.id,
            payable_number=model.payable_number,
            supplier_id=model.supplier_id,
            purchase_order_id=model.purchase_order_id,
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
    
    def _to_model(self, payable: Payable) -> PayableModel:
        return PayableModel(
            id=payable.id,
            payable_number=payable.payable_number,
            supplier_id=payable.supplier_id,
            purchase_order_id=payable.purchase_order_id,
            branch_id=payable.branch_id,
            issue_date=payable.issue_date,
            due_date=payable.due_date,
            total_amount=payable.total_amount,
            paid_amount=payable.paid_amount,
            outstanding_amount=payable.outstanding_amount,
            status=payable.status,
            notes=payable.notes,
            tenant_id=payable.tenant_id,
        )
    
    async def get_by_id(self, payable_id: UUID, tenant_id: UUID) -> Payable | None:
        result = await self.session.execute(
            select(PayableModel).where(
                PayableModel.id == payable_id,
                PayableModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_payable_number(self, payable_number: str, tenant_id: UUID) -> Payable | None:
        result = await self.session.execute(
            select(PayableModel).where(
                PayableModel.payable_number == payable_number,
                PayableModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_purchase_order(self, purchase_order_id: UUID, tenant_id: UUID) -> Payable | None:
        result = await self.session.execute(
            select(PayableModel).where(
                PayableModel.purchase_order_id == purchase_order_id,
                PayableModel.tenant_id == tenant_id,
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
    ) -> list[Payable]:
        result = await self.session.execute(
            select(PayableModel)
            .where(
                PayableModel.supplier_id == supplier_id,
                PayableModel.tenant_id == tenant_id,
            )
            .order_by(PayableModel.issue_date.desc())
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
    ) -> list[Payable]:
        result = await self.session.execute(
            select(PayableModel)
            .where(
                PayableModel.tenant_id == tenant_id,
                PayableModel.due_date < as_of_date,
                PayableModel.status.in_(["open", "partial"]),
            )
            .order_by(PayableModel.due_date.asc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def create(self, payable: Payable) -> Payable:
        model = self._to_model(payable)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, payable: Payable) -> Payable:
        result = await self.session.execute(
            select(PayableModel).where(
                PayableModel.id == payable.id,
                PayableModel.tenant_id == payable.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Payable {payable.id} not found")
        
        model.paid_amount = payable.paid_amount
        model.outstanding_amount = payable.outstanding_amount
        model.status = payable.status
        model.notes = payable.notes
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def apply_payment(
        self,
        payable_id: UUID,
        tenant_id: UUID,
        payment_amount: Decimal,
    ) -> Payable:
        result = await self.session.execute(
            select(PayableModel).where(
                PayableModel.id == payable_id,
                PayableModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Payable {payable_id} not found")
        
        model.paid_amount += payment_amount
        model.outstanding_amount = model.total_amount - model.paid_amount
        
        if model.outstanding_amount <= 0:
            model.status = "paid"
        elif model.paid_amount > 0:
            model.status = "partial"
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)


class SQLAlchemyPayablePaymentRepository(PayablePaymentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: PayablePaymentModel) -> PayablePayment:
        return PayablePayment(
            id=model.id,
            payable_id=model.payable_id,
            payment_id=model.payment_id,
            applied_amount=model.applied_amount,
            applied_date=model.applied_date,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
        )
    
    def _to_model(self, payment: PayablePayment) -> PayablePaymentModel:
        return PayablePaymentModel(
            id=payment.id,
            payable_id=payment.payable_id,
            payment_id=payment.payment_id,
            applied_amount=payment.applied_amount,
            applied_date=payment.applied_date,
            tenant_id=payment.tenant_id,
        )
    
    async def create(self, payment: PayablePayment) -> PayablePayment:
        model = self._to_model(payment)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def list_by_payable(
        self,
        payable_id: UUID,
        tenant_id: UUID,
    ) -> list[PayablePayment]:
        result = await self.session.execute(
            select(PayablePaymentModel).where(
                PayablePaymentModel.payable_id == payable_id,
                PayablePaymentModel.tenant_id == tenant_id,
            )
        )
        return [self._to_domain(model) for model in result.scalars().all()]
