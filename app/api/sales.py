"""
ERP Platform — Sales API Routes

Handles sales order endpoints.
"""

from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.sales_service import SalesService
from app.domain.exceptions import EntityNotFoundException, ValidationException
from app.domain.sales.entities import SalesOrderCreate
from app.infrastructure.database.engine import get_db_session
from app.infrastructure.repositories.sales_repository import (
    SQLAlchemySalesOrderRepository,
    SQLAlchemySalesOrderItemRepository,
)

router = APIRouter(prefix="/sales", tags=["sales"])


# -----------------------------------------------------------------------------
# Request/Response Models
# -----------------------------------------------------------------------------

class SalesOrderItemRequest(BaseModel):
    """Sales order item request."""
    product_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)
    unit_price: Decimal = Field(ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = None


class CreateSalesOrderRequest(BaseModel):
    """Create sales order request."""
    customer_id: UUID
    branch_id: UUID
    order_date: datetime
    items: list[SalesOrderItemRequest]
    tax_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = None


class SalesOrderItemResponse(BaseModel):
    """Sales order item response."""
    id: UUID
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    discount_amount: Decimal
    line_total: Decimal
    notes: str | None


class SalesOrderResponse(BaseModel):
    """Sales order response."""
    id: UUID
    order_number: str
    customer_id: UUID
    branch_id: UUID
    order_date: datetime
    status: str
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    payment_status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime


# -----------------------------------------------------------------------------
# Dependencies
# -----------------------------------------------------------------------------

def get_sales_service(
    session: AsyncSession = Depends(get_db_session),
) -> SalesService:
    """Get sales service with repositories."""
    order_repository = SQLAlchemySalesOrderRepository(session)
    item_repository = SQLAlchemySalesOrderItemRepository(session)
    return SalesService(order_repository, item_repository)


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/orders", response_model=SalesOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_sales_order(
    request: CreateSalesOrderRequest,
    sales_service: SalesService = Depends(get_sales_service),
    # TODO: Get tenant_id and user_id from authentication context
    tenant_id: UUID = UUID("00000000-0000-0000-0000-000000000001"),
    user_id: UUID = UUID("00000000-0000-0000-0000-000000000002"),
):
    """
    Create a new sales order.
    
    - Creates order with line items
    - Calculates totals automatically
    - Returns created order
    """
    try:
        data = SalesOrderCreate(
            customer_id=request.customer_id,
            branch_id=request.branch_id,
            order_date=request.order_date,
            items=[item.model_dump() for item in request.items],
            tax_amount=request.tax_amount,
            discount_amount=request.discount_amount,
            notes=request.notes,
        )
        
        order = await sales_service.create_sales_order(data, user_id, tenant_id)
        
        return SalesOrderResponse(
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
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
    
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/orders/{order_id}", response_model=SalesOrderResponse)
async def get_sales_order(
    order_id: UUID,
    sales_service: SalesService = Depends(get_sales_service),
    tenant_id: UUID = UUID("00000000-0000-0000-0000-000000000001"),
):
    """Get a sales order by ID."""
    try:
        order = await sales_service.get_order(order_id, tenant_id)
        
        return SalesOrderResponse(
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
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
    
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/orders/{order_id}/items", response_model=list[SalesOrderItemResponse])
async def get_sales_order_items(
    order_id: UUID,
    sales_service: SalesService = Depends(get_sales_service),
    tenant_id: UUID = UUID("00000000-0000-0000-0000-000000000001"),
):
    """Get all items for a sales order."""
    items = await sales_service.get_order_items(order_id, tenant_id)
    
    return [
        SalesOrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_amount=item.discount_amount,
            line_total=item.line_total,
            notes=item.notes,
        )
        for item in items
    ]


@router.post("/orders/{order_id}/confirm", response_model=SalesOrderResponse)
async def confirm_sales_order(
    order_id: UUID,
    sales_service: SalesService = Depends(get_sales_service),
    tenant_id: UUID = UUID("00000000-0000-0000-0000-000000000001"),
):
    """Confirm a draft sales order."""
    try:
        order = await sales_service.confirm_order(order_id, tenant_id)
        
        return SalesOrderResponse(
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
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
    
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/customers/{customer_id}/orders", response_model=list[SalesOrderResponse])
async def list_customer_orders(
    customer_id: UUID,
    skip: int = 0,
    limit: int = 100,
    sales_service: SalesService = Depends(get_sales_service),
    tenant_id: UUID = UUID("00000000-0000-0000-0000-000000000001"),
):
    """List sales orders for a customer."""
    orders = await sales_service.list_orders_by_customer(
        customer_id, tenant_id, skip, limit
    )
    
    return [
        SalesOrderResponse(
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
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        for order in orders
    ]
