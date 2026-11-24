"""
ERP Platform — Customer Domain Entities

Customers represent individuals or businesses that purchase products/services.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CustomerType(str, Enum):
    """Customer type."""
    INDIVIDUAL = "individual"
    BUSINESS = "business"
    GOVERNMENT = "government"


class CustomerStatus(str, Enum):
    """Customer status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLACKLISTED = "blacklisted"


class Customer(BaseModel):
    """
    Customer entity.
    
    Represents a buyer of products or services.
    """
    id: UUID
    code: str = Field(min_length=2, max_length=20)  # Unique customer code
    name: str = Field(min_length=1, max_length=200)
    type: CustomerType = CustomerType.INDIVIDUAL
    status: CustomerStatus = CustomerStatus.ACTIVE
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    tax_id: str | None = Field(default=None, max_length=50)
    credit_limit: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    current_balance: Decimal = Field(default=Decimal("0"), decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseModel):
    """Data for creating a new customer."""
    code: str = Field(min_length=2, max_length=20)
    name: str = Field(min_length=1, max_length=200)
    type: CustomerType = CustomerType.INDIVIDUAL
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    tax_id: str | None = Field(default=None, max_length=50)
    credit_limit: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class CustomerUpdate(BaseModel):
    """Data for updating a customer."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    type: CustomerType | None = None
    status: CustomerStatus | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    tax_id: str | None = Field(default=None, max_length=50)
    credit_limit: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class CustomerRepository:
    """Repository interface for Customer entities."""
    
    async def get_by_id(self, customer_id: UUID, tenant_id: UUID) -> Customer | None:
        """Get customer by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_code(self, code: str, tenant_id: UUID) -> Customer | None:
        """Get customer by code within tenant scope."""
        raise NotImplementedError
    
    async def get_by_email(self, email: str, tenant_id: UUID) -> Customer | None:
        """Get customer by email within tenant scope."""
        raise NotImplementedError
    
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Customer]:
        """List customers for a tenant with pagination."""
        raise NotImplementedError
    
    async def create(self, customer: Customer) -> Customer:
        """Create a new customer."""
        raise NotImplementedError
    
    async def update(self, customer: Customer) -> Customer:
        """Update an existing customer."""
        raise NotImplementedError
    
    async def update_balance(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        amount: Decimal,
    ) -> Customer:
        """Update customer balance (for credit/debit operations)."""
        raise NotImplementedError
    
    async def delete(self, customer_id: UUID, tenant_id: UUID) -> bool:
        """Delete a customer."""
        raise NotImplementedError
