"""
ERP Platform — Authentication API Routes

Handles user registration and login endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.authentication_service import AuthenticationService
from app.domain.exceptions import AuthorizationException, EntityAlreadyExistsException
from app.domain.users.entities import UserCreate
from app.infrastructure.database.engine import get_db_session
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository

router = APIRouter(prefix="/auth", tags=["authentication"])


# -----------------------------------------------------------------------------
# Request/Response Models
# -----------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)
    tenant_id: UUID


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str
    tenant_id: UUID


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User data response."""
    id: UUID
    email: str
    username: str
    full_name: str


class RegisterResponse(BaseModel):
    """Registration response with token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginResponse(BaseModel):
    """Login response with token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# -----------------------------------------------------------------------------
# Dependencies
# -----------------------------------------------------------------------------

def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthenticationService:
    """Get authentication service with repository."""
    user_repository = SQLAlchemyUserRepository(session)
    return AuthenticationService(user_repository)


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_service: AuthenticationService = Depends(get_auth_service),
):
    """
    Register a new user.
    
    - Creates a new user account
    - Returns access token for immediate authentication
    """
    try:
        user_data = UserCreate(
            email=request.email,
            username=request.username,
            password=request.password,
            full_name=request.full_name,
            tenant_id=request.tenant_id,
        )
        
        result = await auth_service.register_user(user_data)
        
        return RegisterResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UserResponse(
                id=result["user"].id,
                email=result["user"].email,
                username=result["user"].username,
                full_name=result["user"].full_name,
            ),
        )
    
    except EntityAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with {e.context.get('field')} already exists",
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthenticationService = Depends(get_auth_service),
):
    """
    Authenticate user and return access token.
    
    - Validates email and password
    - Returns JWT access token
    """
    try:
        result = await auth_service.login(
            email=request.email,
            password=request.password,
            tenant_id=request.tenant_id,
        )
        
        return LoginResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UserResponse(**result["user"]),
        )
    
    except AuthorizationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
