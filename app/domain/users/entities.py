"""
ERP Platform — User Domain Entities

Users are the foundation of authentication and authorization.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserStatus(str, Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(BaseModel):
    """
    User entity.
    
    Represents a system user with authentication credentials.
    """
    id: UUID
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password_hash: str = Field(exclude=True)  # Never expose in API
    full_name: str = Field(min_length=1, max_length=200)
    status: UserStatus = UserStatus.ACTIVE
    is_active: bool = True
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    """Data for creating a new user."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)
    tenant_id: UUID


class UserUpdate(BaseModel):
    """Data for updating a user."""
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    status: UserStatus | None = None


class UserRepository:
    """
    Repository interface for User entities.
    
    Domain layer defines the interface; infrastructure implements it.
    """
    
    async def get_by_id(self, user_id: UUID, tenant_id: UUID) -> User | None:
        """Get user by ID within tenant scope."""
        raise NotImplementedError
    
    async def get_by_email(self, email: str, tenant_id: UUID) -> User | None:
        """Get user by email within tenant scope."""
        raise NotImplementedError
    
    async def get_by_username(self, username: str, tenant_id: UUID) -> User | None:
        """Get user by username within tenant scope."""
        raise NotImplementedError
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        raise NotImplementedError
    
    async def update(self, user: User) -> User:
        """Update an existing user."""
        raise NotImplementedError
    
    async def delete(self, user_id: UUID, tenant_id: UUID) -> bool:
        """Delete a user (soft delete recommended)."""
        raise NotImplementedError
