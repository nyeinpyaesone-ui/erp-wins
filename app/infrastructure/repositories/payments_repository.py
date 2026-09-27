"""
ERP Platform — Payments Repository Implementation
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.payments.entities import (
    Payment,
    PaymentAllocation,
    PaymentRepository,
    PaymentAllocationRepository,
    PaymentType,
)
from app.infrastructure.database.models.payments import PaymentModel, PaymentAllocationModel


class SQLAlchemyPaymentRepository(PaymentRepository):
    """SQLAlchemy implementation of PaymentRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: PaymentModel) -> Payment:
        return Payment(
            id=model.id,
            payment_number=model.payment_number,
            payment_type=PaymentType(model.payment_type),
            payment_method=model.payment_method,
            party_id=model.party_id,
            branch_id=model.branch_id,
            payment_date=model.payment_date,
            amount=model.amount,
            status=model.status,
            reference_number=model.reference_number,
            notes=model.notes,
            created_by=model.created_by,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, payment: Payment) -> PaymentModel:
        return PaymentModel(
            id=payment.id,
            payment_number=payment.payment_number,
            payment_type=payment.payment_type.value,
            payment_method=payment.payment_method,
            party_id=payment.party_id,
            branch_id=payment.branch_id,
            payment_date=payment.payment_date,
            amount=payment.amount,
            status=payment.status,
            reference_number=payment.reference_number,
            notes=payment.notes,
            created_by=payment.created_by,
            tenant_id=payment.tenant_id,
        )
    
    async def get_by_id(self, payment_id: UUID, tenant_id: UUID) -> Payment | None:
        result = await self.session.execute(
            select(PaymentModel).where(
                PaymentModel.id == payment_id,
                PaymentModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_payment_number(self, payment_number: str, tenant_id: UUID) -> Payment | None:
        result = await self.session.execute(
            select(PaymentModel).where(
                PaymentModel.payment_number == payment_number,
                PaymentModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def list_by_party(
        self,
        party_id: UUID,
        payment_type: PaymentType,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        result = await self.session.execute(
            select(PaymentModel)
            .where(
                PaymentModel.party_id == party_id,
                PaymentModel.payment_type == payment_type.value,
                PaymentModel.tenant_id == tenant_id,
            )
            .order_by(PaymentModel.payment_date.desc())
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
    ) -> list[Payment]:
        result = await self.session.execute(
            select(PaymentModel)
            .where(
                PaymentModel.branch_id == branch_id,
                PaymentModel.tenant_id == tenant_id,
            )
            .order_by(PaymentModel.payment_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def create(self, payment: Payment) -> Payment:
        model = self._to_model(payment)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, payment: Payment) -> Payment:
        result = await self.session.execute(
            select(PaymentModel).where(
                PaymentModel.id == payment.id,
                PaymentModel.tenant_id == payment.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Payment {payment.id} not found")
        
        model.status = payment.status
        model.notes = payment.notes
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)


class SQLAlchemyPaymentAllocationRepository(PaymentAllocationRepository):
    """SQLAlchemy implementation of PaymentAllocationRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: PaymentAllocationModel) -> PaymentAllocation:
        return PaymentAllocation(
            id=model.id,
            payment_id=model.payment_id,
            invoice_type=model.invoice_type,
            invoice_id=model.invoice_id,
            allocated_amount=model.allocated_amount,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
        )
    
    def _to_model(self, allocation: PaymentAllocation) -> PaymentAllocationModel:
        return PaymentAllocationModel(
            id=allocation.id,
            payment_id=allocation.payment_id,
            invoice_type=allocation.invoice_type,
            invoice_id=allocation.invoice_id,
            allocated_amount=allocation.allocated_amount,
            tenant_id=allocation.tenant_id,
        )
    
    async def create(self, allocation: PaymentAllocation) -> PaymentAllocation:
        model = self._to_model(allocation)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def list_by_payment(self, payment_id: UUID, tenant_id: UUID) -> list[PaymentAllocation]:
        result = await self.session.execute(
            select(PaymentAllocationModel).where(
                PaymentAllocationModel.payment_id == payment_id,
                PaymentAllocationModel.tenant_id == tenant_id,
            )
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def list_by_invoice(
        self,
        invoice_type: str,
        invoice_id: UUID,
        tenant_id: UUID,
    ) -> list[PaymentAllocation]:
        result = await self.session.execute(
            select(PaymentAllocationModel).where(
                PaymentAllocationModel.invoice_type == invoice_type,
                PaymentAllocationModel.invoice_id == invoice_id,
                PaymentAllocationModel.tenant_id == tenant_id,
            )
        )
        return [self._to_domain(model) for model in result.scalars().all()]
