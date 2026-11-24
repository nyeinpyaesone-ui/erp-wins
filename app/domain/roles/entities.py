"""
ERP Platform — Role & Permission Domain Entities

Roles define sets of permissions. Permissions control access to resources.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PermissionAction(str, Enum):
    """Permission actions."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    EXPORT = "export"


class Permission(BaseModel):
    """
    Permission entity.
    
    Defines a specific action on a resource.
    """
    id: UUID
    resource: str = Field(min_length=1, max_length=100)  # e.g., "users", "products"
    action: PermissionAction
    description: str | None = Field(default=None, max_length=500)
    created_at: datetime


class Role(BaseModel):
    """
    Role entity.
    
    Groups permissions together for assignment to users.
    """
    id: UUID
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=2, max_length=50)  # Unique identifier
    description: str | None = Field(default=None, max_length=500)
    is_system: bool = False  # System roles cannot be deleted
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class UserRole(BaseModel):
    """
    User-Role assignment.
    
    Links users to roles within a specific branch scope.
    """
    id: UUID
    user_id: UUID
    role_id: UUID
    branch_id: UUID | None = None  # None means all branches
    tenant_id: UUID
    granted_at: datetime
    granted_by: UUID


class RoleCreate(BaseModel):
    """Data for creating a new role."""
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=500)


class RoleUpdate(BaseModel):
    """Data for updating a role."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class RolePermission(BaseModel):
    """Role-Permission assignment."""
    role_id: UUID
    permission_id: UUID


class RoleRepository:
    """Repository interface for Role entities."""
    
    async def get_by_id(self, role_id: UUID, tenant_id: UUID) -> Role | None:
        """Get role by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_code(self, code: str, tenant_id: UUID) -> Role | None:
        """Get role by code within tenant scope."""
        raise NotImplementedError
    
    async def list_by_tenant(self, tenant_id: UUID) -> list[Role]:
        """List all roles for a tenant."""
        raise NotImplementedError
    
    async def create(self, role: Role) -> Role:
        """Create a new role."""
        raise NotImplementedError
    
    async def update(self, role: Role) -> Role:
        """Update an existing role."""
        raise NotImplementedError
    
    async def delete(self, role_id: UUID, tenant_id: UUID) -> bool:
        """Delete a role (cannot delete system roles)."""
        raise NotImplementedError
    
    async def assign_permission(self, role_id: UUID, permission_id: UUID) -> bool:
        """Assign a permission to a role."""
        raise NotImplementedError
    
    async def revoke_permission(self, role_id: UUID, permission_id: UUID) -> bool:
        """Revoke a permission from a role."""
        raise NotImplementedError
    
    async def get_permissions(self, role_id: UUID) -> list[Permission]:
        """Get all permissions for a role."""
        raise NotImplementedError


class UserRoleRepository:
    """Repository interface for User-Role assignments."""
    
    async def assign_role(
        self,
        user_id: UUID,
        role_id: UUID,
        branch_id: UUID | None,
        tenant_id: UUID,
        granted_by: UUID,
    ) -> UserRole:
        """Assign a role to a user."""
        raise NotImplementedError
    
    async def revoke_role(self, user_id: UUID, role_id: UUID, tenant_id: UUID) -> bool:
        """Revoke a role from a user."""
        raise NotImplementedError
    
    async def get_user_roles(self, user_id: UUID, tenant_id: UUID) -> list[UserRole]:
        """Get all roles for a user."""
        raise NotImplementedError
    
    async def get_role_users(self, role_id: UUID, tenant_id: UUID) -> list[UUID]:
        """Get all users with a specific role."""
        raise NotImplementedError
