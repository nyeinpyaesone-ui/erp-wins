"""
ERP Platform — Authentication Infrastructure

Password hashing and JWT token management.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from passlib.context import CryptContext

from app.config import get_settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: UUID,
    tenant_id: UUID,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: User ID
        tenant_id: Tenant ID
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    settings = get_settings()
    
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.jwt_expiration_minutes)
    
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    
    to_encode = {
        "sub": str(user_id),
        "tenant_id": str(tenant_id),
        "exp": expire,
        "iat": now,
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.app_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: JWT token string
    
    Returns:
        Token payload dictionary
    
    Raises:
        jwt.ExpiredSignatureError: Token has expired
        jwt.InvalidTokenError: Token is invalid
    """
    settings = get_settings()
    
    payload = jwt.decode(
        token,
        settings.app_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    
    return payload
