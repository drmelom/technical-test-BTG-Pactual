from typing import Optional
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.models import User, UserRole
from app.repositories.user_repository import user_repository
from app.core.security import security
from app.api.schemas import UserCreate, UserUpdate, Token


class AuthService:
    """Service for authentication operations."""
    
    async def register(self, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = await user_repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        try:
            user = await user_repository.create(
                email=user_data.email,
                password=user_data.password,
                full_name=user_data.full_name,
                phone=user_data.phone,
                notification_preference=user_data.notification_preference
            )
            return user
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def authenticate(self, email: str, password: str) -> Token:
        """Authenticate user and return tokens."""
        user = await user_repository.authenticate(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=30)  # 30 minutes
        refresh_token_expires = timedelta(days=7)     # 7 days
        
        access_token = security.create_access_token(
            subject=str(user.id),
            expires_delta=access_token_expires
        )
        
        refresh_token = security.create_refresh_token(
            subject=str(user.id),
            expires_delta=refresh_token_expires
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    async def refresh_token(self, refresh_token: str) -> Token:
        """Refresh access token using refresh token."""
        try:
            user_id = security.validate_refresh_token(refresh_token)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Verify user still exists and is active
        user = await user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        access_token_expires = timedelta(minutes=30)
        refresh_token_expires = timedelta(days=7)
        
        new_access_token = security.create_access_token(
            subject=user_id,
            expires_delta=access_token_expires
        )
        
        new_refresh_token = security.create_refresh_token(
            subject=user_id,
            expires_delta=refresh_token_expires
        )
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )


class UserService:
    """Service for user operations."""
    
    async def get_profile(self, user_id: str) -> User:
        """Get user profile."""
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    async def update_profile(self, user_id: str, user_data: UserUpdate) -> User:
        """Update user profile."""
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_data.model_dump(exclude_unset=True)
        updated_user = await user_repository.update(user_id, **update_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user"
            )
        
        return updated_user
    
    async def get_balance(self, user_id: str) -> dict:
        """Get user balance."""
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "current_balance": user.current_balance,
            "currency": "COP"
        }


# Create service instances
auth_service = AuthService()
user_service = UserService()
