from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.api.deps import get_current_active_user
from app.api.schemas import (
    UserResponse, 
    UserUpdate, 
    BalanceResponse,
    APIResponse,
    UserFundSubscriptionResponse
)
from app.models import User
from app.services.auth_service import user_service
from app.services.fund_service import fund_service


router = APIRouter()


@router.get("/me", response_model=APIResponse)
async def get_current_user(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    user_data = {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "phone_number": current_user.phone_number,
        "role": current_user.role,
        "current_balance": str(current_user.current_balance),
        "notification_preference": current_user.notification_preference,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat(),
        "updated_at": current_user.updated_at.isoformat()
    }
    
    return APIResponse(
        success=True,
        message="User profile retrieved successfully",
        data=user_data
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile."""
    return await user_service.update_profile(str(current_user.id), user_data)


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user balance."""
    return await user_service.get_balance(str(current_user.id))


@router.get("/subscriptions", response_model=list[UserFundSubscriptionResponse])
async def get_subscriptions(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user fund subscriptions."""
    subscriptions = await fund_service.get_user_subscriptions(str(current_user.id))
    return subscriptions
