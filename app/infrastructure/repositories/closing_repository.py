"""
ERP Platform — Daily Closing Repository Implementation
"""

from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.closing.entities import DailyClosing, DailyClosingRepository
from app.infrastructure.database.models.closing import DailyClosingModel


class SQLAlchemyDailyClosingRepository(DailyClosingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: DailyClosingModel) -> DailyClosing:
        return DailyClosing(
            id=model.id,
            closing_number=model.closing_number,
            branch_id=model.branch_id,
            closing_date=model.closing_date,
            status=model.status,
            total_sales=model.total_sales,
            sales_count=model.sales_count,
            total_purchases=model.total_purchases,
            purchase_count=model.purchase_count,
            total_customer_payments=model.total_customer_payments,
            customer_payment_count=model.customer_payment_count,
            total_supplier_payments=model.total_supplier_payments,
            supplier_payment_count=model.supplier_payment_count,
            opening_cash=model.opening_cash,
            closing_cash=model.closing_cash,
            expected_cash=model.expected_cash,
            cash_difference=model.cash_difference,
            notes=model.notes,
            created_by=model.created_by,
            approved_by=model.approved_by,
            approved_at=model.approved_at,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, closing: DailyClosing) -> DailyClosingModel:
        return DailyClosingModel(
            id=closing.id,
            closing_number=closing.closing_number,
            branch_id=closing.branch_id,
            closing_date=closing.closing_date,
            status=closing.status,
            total_sales=closing.total_sales,
            sales_count=closing.sales_count,
            total_purchases=closing.total_purchases,
            purchase_count=closing.purchase_count,
            total_customer_payments=closing.total_customer_payments,
            customer_payment_count=closing.customer_payment_count,
            total_supplier_payments=closing.total_supplier_payments,
            supplier_payment_count=closing.supplier_payment_count,
            opening_cash=closing.opening_cash,
            closing_cash=closing.closing_cash,
            expected_cash=closing.expected_cash,
            cash_difference=closing.cash_difference,
            notes=closing.notes,
            created_by=closing.created_by,
            approved_by=closing.approved_by,
            approved_at=closing.approved_at,
            tenant_id=closing.tenant_id,
        )
    
    async def get_by_id(self, closing_id: UUID, tenant_id: UUID) -> DailyClosing | None:
        result = await self.session.execute(
            select(DailyClosingModel).where(
                DailyClosingModel.id == closing_id,
                DailyClosingModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_closing_number(self, closing_number: str, tenant_id: UUID) -> DailyClosing | None:
        result = await self.session.execute(
            select(DailyClosingModel).where(
                DailyClosingModel.closing_number == closing_number,
                DailyClosingModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_branch_and_date(
        self,
        branch_id: UUID,
        closing_date: date,
        tenant_id: UUID,
    ) -> DailyClosing | None:
        result = await self.session.execute(
            select(DailyClosingModel).where(
                DailyClosingModel.branch_id == branch_id,
                DailyClosingModel.closing_date == closing_date,
                DailyClosingModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DailyClosing]:
        result = await self.session.execute(
            select(DailyClosingModel)
            .where(
                DailyClosingModel.branch_id == branch_id,
                DailyClosingModel.tenant_id == tenant_id,
            )
            .order_by(DailyClosingModel.closing_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]
    
    async def create(self, closing: DailyClosing) -> DailyClosing:
        model = self._to_model(closing)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, closing: DailyClosing) -> DailyClosing:
        result = await self.session.execute(
            select(DailyClosingModel).where(
                DailyClosingModel.id == closing.id,
                DailyClosingModel.tenant_id == closing.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"DailyClosing {closing.id} not found")
        
        model.status = closing.status
        model.closing_cash = closing.closing_cash
        model.expected_cash = closing.expected_cash
        model.cash_difference = closing.cash_difference
        model.notes = closing.notes
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def approve(
        self,
        closing_id: UUID,
        tenant_id: UUID,
        approved_by: UUID,
    ) -> DailyClosing:
        result = await self.session.execute(
            select(DailyClosingModel).where(
                DailyClosingModel.id == closing_id,
                DailyClosingModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"DailyClosing {closing_id} not found")
        
        model.status = "approved"
        model.approved_by = approved_by
        model.approved_at = datetime.now()
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
