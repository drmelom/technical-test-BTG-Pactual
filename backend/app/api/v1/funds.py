from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from decimal import Decimal

from app.api.deps import get_current_active_user
from app.api.schemas import (
    FundResponse,
    SubscriptionRequest,
    CancellationRequest,
    APIResponse
)
from app.models import User
from app.services.fund_service import fund_service


router = APIRouter()


@router.get("/", response_model=APIResponse)
async def get_funds(
    current_user: User = Depends(get_current_active_user)
):
    """Get all available funds."""
    funds = await fund_service.get_all_funds(is_active=True)
    return APIResponse(
        success=True,
        message="Funds retrieved successfully",
        data=funds
    )


@router.get("/{fund_id}", response_model=FundResponse)
async def get_fund(
    fund_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get fund by ID."""
    return await fund_service.get_fund_by_id(fund_id)


@router.post("/subscribe", response_model=APIResponse)
async def subscribe_to_fund(
    subscription_data: SubscriptionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Subscribe to a fund."""
    result = await fund_service.subscribe_to_fund(
        user_id=str(current_user.id),
        fund_id=subscription_data.fund_id,
        amount=subscription_data.amount
    )
    
    return APIResponse(
        success=result["success"],
        message=result["message"],
        data={
            "transaction_id": result["transaction_id"],
            "amount": result["amount"],
            "new_balance": result["new_balance"]
        }
    )


@router.post("/cancel", response_model=APIResponse)
async def cancel_subscription(
    cancellation_data: CancellationRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Cancel fund subscription."""
    result = await fund_service.cancel_subscription(
        user_id=str(current_user.id),
        fund_id=cancellation_data.fund_id
    )
    
    return APIResponse(
        success=result["success"],
        message=result["message"],
        data={
            "transaction_id": result["transaction_id"],
            "refunded_amount": result["refunded_amount"],
            "new_balance": result["new_balance"]
        }
    )
