"""
ERP Platform — Product Domain Entities

Products represent items that can be sold or used in inventory.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ProductType(str, Enum):
    """Product type."""
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SERVICE = "service"


class ProductStatus(str, Enum):
    """Product status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class Product(BaseModel):
    """
    Product entity.
    
    Represents an item in the catalog.
    """
    id: UUID
    sku: str = Field(min_length=1, max_length=50)  # Stock Keeping Unit
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    type: ProductType = ProductType.PHYSICAL
    status: ProductStatus = ProductStatus.ACTIVE
    category_id: UUID | None = None
    unit_of_measure: str = Field(default="piece", max_length=20)
    barcode: str | None = Field(default=None, max_length=50)
    cost_price: Decimal = Field(ge=0, decimal_places=2)
    selling_price: Decimal = Field(ge=0, decimal_places=2)
    is_trackable: bool = True  # Whether to track inventory
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    """Data for creating a new product."""
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    type: ProductType = ProductType.PHYSICAL
    category_id: UUID | None = None
    unit_of_measure: str = Field(default="piece", max_length=20)
    barcode: str | None = Field(default=None, max_length=50)
    cost_price: Decimal = Field(ge=0, decimal_places=2)
    selling_price: Decimal = Field(ge=0, decimal_places=2)
    is_trackable: bool = True


class ProductUpdate(BaseModel):
    """Data for updating a product."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    type: ProductType | None = None
    status: ProductStatus | None = None
    category_id: UUID | None = None
    unit_of_measure: str | None = Field(default=None, max_length=20)
    barcode: str | None = Field(default=None, max_length=50)
    cost_price: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    selling_price: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    is_trackable: bool | None = None


class ProductRepository:
    """Repository interface for Product entities."""
    
    async def get_by_id(self, product_id: UUID, tenant_id: UUID) -> Product | None:
        """Get product by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_sku(self, sku: str, tenant_id: UUID) -> Product | None:
        """Get product by SKU within tenant scope."""
        raise NotImplementedError
    
    async def get_by_barcode(self, barcode: str, tenant_id: UUID) -> Product | None:
        """Get product by barcode within tenant scope."""
        raise NotImplementedError
    
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        """List products for a tenant with pagination."""
        raise NotImplementedError
    
    async def create(self, product: Product) -> Product:
        """Create a new product."""
        raise NotImplementedError
    
    async def update(self, product: Product) -> Product:
        """Update an existing product."""
        raise NotImplementedError
    
    async def delete(self, product_id: UUID, tenant_id: UUID) -> bool:
        """Delete a product."""
        raise NotImplementedError
