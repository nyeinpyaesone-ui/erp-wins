"""
ERP Platform — Supplier Domain Entities

Suppliers represent businesses that provide products or services.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SupplierType(str, Enum):
    """Supplier type."""
    MANUFACTURER = "manufacturer"
    DISTRIBUTOR = "distributor"
    WHOLESALER = "wholesaler"
    RETAILER = "retailer"
    SERVICE_PROVIDER = "service_provider"


class SupplierStatus(str, Enum):
    """Supplier status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLACKLISTED = "blacklisted"


class Supplier(BaseModel):
    """
    Supplier entity.
    
    Represents a vendor of products or services.
    """
    id: UUID
    code: str = Field(min_length=2, max_length=20)  # Unique supplier code
    name: str = Field(min_length=1, max_length=200)
    type: SupplierType = SupplierType.DISTRIBUTOR
    status: SupplierStatus = SupplierStatus.ACTIVE
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    tax_id: str | None = Field(default=None, max_length=50)
    payment_terms: str | None = Field(default=None, max_length=200)
    credit_limit: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    current_balance: Decimal = Field(default=Decimal("0"), decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class SupplierCreate(BaseModel):
    """Data for creating a new supplier."""
    code: str = Field(min_length=2, max_length=20)
    name: str = Field(min_length=1, max_length=200)
    type: SupplierType = SupplierType.DISTRIBUTOR
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    tax_id: str | None = Field(default=None, max_length=50)
    payment_terms: str | None = Field(default=None, max_length=200)
    credit_limit: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class SupplierUpdate(BaseModel):
    """Data for updating a supplier."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    type: SupplierType | None = None
    status: SupplierStatus | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    tax_id: str | None = Field(default=None, max_length=50)
    payment_terms: str | None = Field(default=None, max_length=200)
    credit_limit: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class SupplierRepository:
    """Repository interface for Supplier entities."""
    
    async def get_by_id(self, supplier_id: UUID, tenant_id: UUID) -> Supplier | None:
        """Get supplier by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_code(self, code: str, tenant_id: UUID) -> Supplier | None:
        """Get supplier by code within tenant scope."""
        raise NotImplementedError
    
    async def get_by_email(self, email: str, tenant_id: UUID) -> Supplier | None:
        """Get supplier by email within tenant scope."""
        raise NotImplementedError
    
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Supplier]:
        """List suppliers for a tenant with pagination."""
        raise NotImplementedError
    
    async def create(self, supplier: Supplier) -> Supplier:
        """Create a new supplier."""
        raise NotImplementedError
    
    async def update(self, supplier: Supplier) -> Supplier:
        """Update an existing supplier."""
        raise NotImplementedError
    
    async def update_balance(
        self,
        supplier_id: UUID,
        tenant_id: UUID,
        amount: Decimal,
    ) -> Supplier:
        """Update supplier balance (for payable operations)."""
        raise NotImplementedError
    
    async def delete(self, supplier_id: UUID, tenant_id: UUID) -> bool:
        """Delete a supplier."""
        raise NotImplementedError
