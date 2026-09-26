"""
ERP Platform — User Repository Implementation

SQLAlchemy implementation of UserRepository interface.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users.entities import User, UserRepository
from app.infrastructure.database.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of UserRepository.
    
    All operations are scoped to tenant_id for multi-tenancy.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity."""
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            password_hash=model.password_hash,
            full_name=model.full_name,
            status=model.status,
            is_active=model.is_active,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, user: User) -> UserModel:
        """Convert domain entity to SQLAlchemy model."""
        return UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            password_hash=user.password_hash,
            full_name=user.full_name,
            status=user.status,
            is_active=user.is_active,
            tenant_id=user.tenant_id,
        )
    
    async def get_by_id(self, user_id: UUID, tenant_id: UUID) -> User | None:
        """Get user by ID within tenant scope."""
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.id == user_id,
                UserModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_email(self, email: str, tenant_id: UUID) -> User | None:
        """Get user by email within tenant scope."""
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.email == email,
                UserModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_username(self, username: str, tenant_id: UUID) -> User | None:
        """Get user by username within tenant scope."""
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.username == username,
                UserModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        model = self._to_model(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, user: User) -> User:
        """Update an existing user."""
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.id == user.id,
                UserModel.tenant_id == user.tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"User {user.id} not found")
        
        # Update fields
        if user.email:
            model.email = user.email
        if user.username:
            model.username = user.username
        if user.full_name:
            model.full_name = user.full_name
        if user.status:
            model.status = user.status
        model.is_active = user.is_active
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def delete(self, user_id: UUID, tenant_id: UUID) -> bool:
        """Delete a user (soft delete recommended)."""
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.id == user_id,
                UserModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        # Soft delete
        model.is_active = False
        model.status = "inactive"
        await self.session.flush()
        return True
