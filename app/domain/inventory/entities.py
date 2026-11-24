"""
ERP Platform — Inventory Domain Entities

Inventory manages stock levels, movements, and reservations.
Stock-changing operations are transactional.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class StockMovementType(str, Enum):
    """Types of stock movements."""
    RECEIPT = "receipt"  # Stock in from supplier
    SALE = "sale"  # Stock out for sale
    RETURN_IN = "return_in"  # Customer return
    RETURN_OUT = "return_out"  # Return to supplier
    ADJUSTMENT_IN = "adjustment_in"  # Manual increase
    ADJUSTMENT_OUT = "adjustment_out"  # Manual decrease
    TRANSFER_OUT = "transfer_out"  # Transfer to another location
    TRANSFER_IN = "transfer_in"  # Receive transfer
    RESERVATION = "reservation"  # Reserve stock
    RESERVATION_RELEASE = "reservation_release"  # Release reservation


class StockStatus(str, Enum):
    """Stock status."""
    AVAILABLE = "available"
    RESERVED = "reserved"
    DAMAGED = "damaged"
    QUARANTINED = "quarantined"


class Stock(BaseModel):
    """
    Stock entity.
    
    Represents current inventory level for a product at a location.
    """
    id: UUID
    product_id: UUID
    branch_id: UUID  # Location/warehouse
    quantity: Decimal = Field(ge=0, decimal_places=4)
    reserved_quantity: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=4)
    available_quantity: Decimal = Field(ge=0, decimal_places=4)
    unit_of_measure: str = Field(max_length=20)
    status: StockStatus = StockStatus.AVAILABLE
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class StockMovement(BaseModel):
    """
    Stock movement entity.
    
    Records every change in inventory for audit trail.
    """
    id: UUID
    product_id: UUID
    branch_id: UUID
    movement_type: StockMovementType
    quantity: Decimal = Field(decimal_places=4)
    reference_type: str | None = Field(default=None, max_length=50)  # e.g., "sale", "purchase"
    reference_id: UUID | None = None  # ID of the related document
    notes: str | None = Field(default=None, max_length=500)
    performed_by: UUID  # User who performed the movement
    tenant_id: UUID
    created_at: datetime


class StockReservation(BaseModel):
    """
    Stock reservation entity.
    
    Reserves stock for a specific order or purpose.
    """
    id: UUID
    product_id: UUID
    branch_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)
    reserved_by: UUID  # User who made the reservation
    reference_type: str = Field(max_length=50)  # e.g., "sale_order"
    reference_id: UUID  # ID of the related document
    expires_at: datetime | None = None  # Auto-release after expiration
    is_released: bool = False
    released_at: datetime | None = None
    tenant_id: UUID
    created_at: datetime


class StockCreate(BaseModel):
    """Data for creating initial stock."""
    product_id: UUID
    branch_id: UUID
    quantity: Decimal = Field(ge=0, decimal_places=4)
    unit_of_measure: str = Field(max_length=20)


class StockAdjustment(BaseModel):
    """Data for stock adjustment."""
    product_id: UUID
    branch_id: UUID
    quantity_change: Decimal = Field(decimal_places=4)  # Positive or negative
    notes: str | None = Field(default=None, max_length=500)


class StockTransfer(BaseModel):
    """Data for stock transfer between branches."""
    product_id: UUID
    from_branch_id: UUID
    to_branch_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)
    notes: str | None = Field(default=None, max_length=500)


class StockRepository:
    """Repository interface for Stock entities."""
    
    async def get_by_id(self, stock_id: UUID, tenant_id: UUID) -> Stock | None:
        """Get stock by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_product_and_branch(
        self,
        product_id: UUID,
        branch_id: UUID,
        tenant_id: UUID,
    ) -> Stock | None:
        """Get stock for a specific product at a specific branch."""
        raise NotImplementedError
    
    async def list_by_product(
        self,
        product_id: UUID,
        tenant_id: UUID,
    ) -> list[Stock]:
        """List all stock records for a product across branches."""
        raise NotImplementedError
    
    async def list_by_branch(
        self,
        branch_id: UUID,
        tenant_id: UUID,
    ) -> list[Stock]:
        """List all stock at a specific branch."""
        raise NotImplementedError
    
    async def create(self, stock: Stock) -> Stock:
        """Create initial stock record."""
        raise NotImplementedError
    
    async def update_quantity(
        self,
        stock_id: UUID,
        tenant_id: UUID,
        quantity_change: Decimal,
    ) -> Stock:
        """Update stock quantity (must be transactional)."""
        raise NotImplementedError
    
    async def reserve_quantity(
        self,
        stock_id: UUID,
        tenant_id: UUID,
        quantity: Decimal,
    ) -> Stock:
        """Reserve stock (must be transactional)."""
        raise NotImplementedError
    
    async def release_reservation(
        self,
        stock_id: UUID,
        tenant_id: UUID,
        quantity: Decimal,
    ) -> Stock:
        """Release reserved stock (must be transactional)."""
        raise NotImplementedError


class StockMovementRepository:
    """Repository interface for StockMovement entities."""
    
    async def create(self, movement: StockMovement) -> StockMovement:
        """Create a stock movement record."""
        raise NotImplementedError
    
    async def list_by_product(
        self,
        product_id: UUID,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[StockMovement]:
        """List movements for a product with pagination."""
        raise NotImplementedError
    
    async def list_by_reference(
        self,
        reference_type: str,
        reference_id: UUID,
        tenant_id: UUID,
    ) -> list[StockMovement]:
        """List movements for a specific reference document."""
        raise NotImplementedError


class StockReservationRepository:
    """Repository interface for StockReservation entities."""
    
    async def create(self, reservation: StockReservation) -> StockReservation:
        """Create a stock reservation."""
        raise NotImplementedError
    
    async def release(self, reservation_id: UUID, tenant_id: UUID) -> StockReservation:
        """Release a reservation."""
        raise NotImplementedError
    
    async def get_by_reference(
        self,
        reference_type: str,
        reference_id: UUID,
        tenant_id: UUID,
    ) -> list[StockReservation]:
        """Get reservations for a specific reference."""
        raise NotImplementedError
    
    async def list_expired(self, tenant_id: UUID) -> list[StockReservation]:
        """List expired reservations that need to be released."""
        raise NotImplementedError
