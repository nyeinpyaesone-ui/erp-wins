"""
ERP Platform — Authentication Application Service

Handles user authentication and token management.
"""

from uuid import UUID

from app.domain.exceptions import AuthorizationException, EntityNotFoundException
from app.domain.users.entities import UserCreate, UserRepository
from app.infrastructure.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthenticationService:
    """
    Application service for authentication.
    
    Handles login, registration, and token management.
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def register_user(self, data: UserCreate) -> dict:
        """
        Register a new user.
        
        Args:
            data: User registration data
        
        Returns:
            User data and access token
        
        Raises:
            EntityAlreadyExistsException: If email or username already exists
        """
        # Check if email already exists
        existing_user = await self.user_repository.get_by_email(
            data.email, data.tenant_id
        )
        if existing_user:
            from app.domain.exceptions import EntityAlreadyExistsException
            raise EntityAlreadyExistsException("User", "email", data.email)
        
        # Check if username already exists
        existing_user = await self.user_repository.get_by_username(
            data.username, data.tenant_id
        )
        if existing_user:
            from app.domain.exceptions import EntityAlreadyExistsException
            raise EntityAlreadyExistsException("User", "username", data.username)
        
        # Hash password
        password_hash = hash_password(data.password)
        
        # Create user
        from datetime import datetime, timezone
        from uuid import uuid4
        
        user = await self.user_repository.create(
            User(
                id=uuid4(),
                email=data.email,
                username=data.username,
                password_hash=password_hash,
                full_name=data.full_name,
                tenant_id=data.tenant_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
        )
        
        # Generate access token
        access_token = create_access_token(user.id, user.tenant_id)
        
        return {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer",
        }
    
    async def login(self, email: str, password: str, tenant_id: UUID) -> dict:
        """
        Authenticate a user and return access token.
        
        Args:
            email: User email
            password: Plain text password
            tenant_id: Tenant ID
        
        Returns:
            Access token and user data
        
        Raises:
            AuthorizationException: If credentials are invalid
        """
        # Find user by email
        user = await self.user_repository.get_by_email(email, tenant_id)
        if not user:
            raise AuthorizationException("Invalid email or password")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise AuthorizationException("Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            raise AuthorizationException("User account is inactive")
        
        # Generate access token
        access_token = create_access_token(user.id, user.tenant_id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
            },
        }
