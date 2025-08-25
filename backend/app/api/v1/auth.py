from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.api.schemas import (
    UserLogin, 
    UserCreate, 
    UserResponse, 
    Token, 
    APIResponse
)
from app.services.auth_service import auth_service
from app.core.security import security


router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user."""
    user = await auth_service.register(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return access tokens."""
    return await auth_service.authenticate(
        user_credentials.email, 
        user_credentials.password
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security.security)
):
    """Refresh access token using refresh token."""
    refresh_token = credentials.credentials
    return await auth_service.refresh_token(refresh_token)


@router.post("/logout", response_model=APIResponse)
async def logout():
    """Logout user (client-side token removal)."""
    return APIResponse(
        success=True,
        message="Successfully logged out. Please remove tokens from client storage."
    )
