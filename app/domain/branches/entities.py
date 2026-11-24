"""
ERP Platform — Branch Domain Entities

Branches represent physical or logical locations within an organization.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class BranchType(str, Enum):
    """Branch type."""
    HEADQUARTERS = "headquarters"
    BRANCH = "branch"
    WAREHOUSE = "warehouse"
    RETAIL = "retail"


class Branch(BaseModel):
    """
    Branch entity.
    
    Represents a location within an organization.
    """
    id: UUID
    organization_id: UUID
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=2, max_length=20)  # Unique within organization
    type: BranchType = BranchType.BRANCH
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    is_active: bool = True
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class BranchCreate(BaseModel):
    """Data for creating a new branch."""
    organization_id: UUID
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=2, max_length=20)
    type: BranchType = BranchType.BRANCH
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)


class BranchUpdate(BaseModel):
    """Data for updating a branch."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    type: BranchType | None = None
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=254)
    is_active: bool | None = None


class BranchRepository:
    """Repository interface for Branch entities."""
    
    async def get_by_id(self, branch_id: UUID, tenant_id: UUID) -> Branch | None:
        """Get branch by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_code(self, code: str, organization_id: UUID) -> Branch | None:
        """Get branch by code within organization."""
        raise NotImplementedError
    
    async def list_by_organization(self, organization_id: UUID) -> list[Branch]:
        """List all branches for an organization."""
        raise NotImplementedError
    
    async def create(self, branch: Branch) -> Branch:
        """Create a new branch."""
        raise NotImplementedError
    
    async def update(self, branch: Branch) -> Branch:
        """Update an existing branch."""
        raise NotImplementedError
    
    async def delete(self, branch_id: UUID, tenant_id: UUID) -> bool:
        """Delete a branch."""
        raise NotImplementedError
