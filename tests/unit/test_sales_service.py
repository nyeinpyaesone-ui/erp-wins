"""
ERP Platform — Sales Service Unit Tests

Tests for sales order business logic.
"""

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4, UUID

import pytest

from app.application.services.sales_service import SalesService
from app.domain.sales.entities import (
    SalesOrder,
    SalesOrderCreate,
    SalesOrderStatus,
)
from app.domain.exceptions import EntityNotFoundException, ValidationException


# Mock repositories for testing
class MockSalesOrderRepository:
    def __init__(self):
        self.orders = {}
    
    async def get_by_id(self, order_id: UUID, tenant_id: UUID) -> SalesOrder | None:
        return self.orders.get(order_id)
    
    async def create(self, order: SalesOrder) -> SalesOrder:
        self.orders[order.id] = order
        return order
    
    async def update(self, order: SalesOrder) -> SalesOrder:
        self.orders[order.id] = order
        return order
    
    async def list_by_customer(self, customer_id: UUID, tenant_id: UUID, skip: int = 0, limit: int = 100):
        return [o for o in self.orders.values() if o.customer_id == customer_id]
    
    async def list_by_branch(self, branch_id: UUID, tenant_id: UUID, skip: int = 0, limit: int = 100):
        return [o for o in self.orders.values() if o.branch_id == branch_id]


class MockSalesOrderItemRepository:
    def __init__(self):
        self.items = []
    
    async def create(self, item):
        self.items.append(item)
        return item
    
    async def list_by_order(self, order_id: UUID, tenant_id: UUID):
        return [i for i in self.items if i.sales_order_id == order_id]


@pytest.fixture
def sales_service():
    """Create sales service with mock repositories."""
    order_repo = MockSalesOrderRepository()
    item_repo = MockSalesOrderItemRepository()
    return SalesService(order_repo, item_repo)


@pytest.fixture
def tenant_id():
    return uuid4()


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def customer_id():
    return uuid4()


@pytest.fixture
def branch_id():
    return uuid4()


@pytest.fixture
def product_id():
    return uuid4()


@pytest.mark.asyncio
async def test_create_sales_order(sales_service, tenant_id, user_id, customer_id, branch_id, product_id):
    """Test creating a sales order with items."""
    data = SalesOrderCreate(
        customer_id=customer_id,
        branch_id=branch_id,
        order_date=datetime.now(timezone.utc),
        items=[
            {
                "product_id": str(product_id),
                "quantity": "10",
                "unit_price": "100.00",
                "discount_amount": "50.00",
            }
        ],
        tax_amount=Decimal("50.00"),
        discount_amount=Decimal("0.00"),
        notes="Test order",
    )
    
    order = await sales_service.create_sales_order(data, user_id, tenant_id)
    
    assert order is not None
    assert order.customer_id == customer_id
    assert order.branch_id == branch_id
    assert order.status == SalesOrderStatus.DRAFT
    assert order.subtotal == Decimal("950.00")  # (10 * 100) - 50
    assert order.tax_amount == Decimal("50.00")
    assert order.total_amount == Decimal("1000.00")  # 950 + 50
    assert order.payment_status == "pending"
    assert order.order_number.startswith("SO-")


@pytest.mark.asyncio
async def test_confirm_sales_order(sales_service, tenant_id, user_id, customer_id, branch_id, product_id):
    """Test confirming a draft sales order."""
    # Create order first
    data = SalesOrderCreate(
        customer_id=customer_id,
        branch_id=branch_id,
        order_date=datetime.now(timezone.utc),
        items=[
            {
                "product_id": str(product_id),
                "quantity": "5",
                "unit_price": "200.00",
                "discount_amount": "0.00",
            }
        ],
    )
    
    order = await sales_service.create_sales_order(data, user_id, tenant_id)
    assert order.status == SalesOrderStatus.DRAFT
    
    # Confirm order
    confirmed_order = await sales_service.confirm_order(order.id, tenant_id)
    
    assert confirmed_order.status == SalesOrderStatus.CONFIRMED


@pytest.mark.asyncio
async def test_confirm_non_draft_order_fails(sales_service, tenant_id, user_id, customer_id, branch_id, product_id):
    """Test that confirming a non-draft order fails."""
    # Create and confirm order
    data = SalesOrderCreate(
        customer_id=customer_id,
        branch_id=branch_id,
        order_date=datetime.now(timezone.utc),
        items=[
            {
                "product_id": str(product_id),
                "quantity": "1",
                "unit_price": "100.00",
            }
        ],
    )
    
    order = await sales_service.create_sales_order(data, user_id, tenant_id)
    await sales_service.confirm_order(order.id, tenant_id)
    
    # Try to confirm again - should fail
    with pytest.raises(ValidationException):
        await sales_service.confirm_order(order.id, tenant_id)


@pytest.mark.asyncio
async def test_get_nonexistent_order_fails(sales_service, tenant_id):
    """Test that getting a nonexistent order raises exception."""
    fake_id = uuid4()
    
    with pytest.raises(EntityNotFoundException):
        await sales_service.get_order(fake_id, tenant_id)


@pytest.mark.asyncio
async def test_list_orders_by_customer(sales_service, tenant_id, user_id, customer_id, branch_id, product_id):
    """Test listing orders by customer."""
    # Create multiple orders
    for i in range(3):
        data = SalesOrderCreate(
            customer_id=customer_id,
            branch_id=branch_id,
            order_date=datetime.now(timezone.utc),
            items=[
                {
                    "product_id": str(product_id),
                    "quantity": str(i + 1),
                    "unit_price": "100.00",
                }
            ],
        )
        await sales_service.create_sales_order(data, user_id, tenant_id)
    
    # List orders
    orders = await sales_service.list_orders_by_customer(customer_id, tenant_id)
    
    assert len(orders) == 3
    assert all(o.customer_id == customer_id for o in orders)
