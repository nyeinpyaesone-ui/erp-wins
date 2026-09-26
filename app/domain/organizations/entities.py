"""
ERP Platform — Organization Domain Entities

Organizations represent companies or businesses using the system.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class OrganizationType(str, Enum):
    """Organization type."""
    COMPANY = "company"
    INDIVIDUAL = "individual"
    NONPROFIT = "nonprofit"
    GOVERNMENT = "government"


class Organization(BaseModel):
    """
    Organization entity.
    
    Represents a tenant in the multi-tenant system.
    """
    id: UUID
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=2, max_length=20)  # Unique identifier code
    type: OrganizationType = OrganizationType.COMPANY
    tax_id: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class OrganizationCreate(BaseModel):
    """Data for creating a new organization."""
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=2, max_length=20)
    type: OrganizationType = OrganizationType.COMPANY
    tax_id: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)


class OrganizationUpdate(BaseModel):
    """Data for updating an organization."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    tax_id: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    is_active: bool | None = None


class OrganizationRepository:
    """Repository interface for Organization entities."""
    
    async def get_by_id(self, org_id: UUID) -> Organization | None:
        """Get organization by ID."""
        raise NotImplementedError
    
    async def get_by_code(self, code: str) -> Organization | None:
        """Get organization by unique code."""
        raise NotImplementedError
    
    async def create(self, org: Organization) -> Organization:
        """Create a new organization."""
        raise NotImplementedError
    
    async def update(self, org: Organization) -> Organization:
        """Update an existing organization."""
        raise NotImplementedError
    
    async def delete(self, org_id: UUID) -> bool:
        """Delete an organization."""
        raise NotImplementedError
