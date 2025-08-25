from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.api.deps import get_current_active_user, get_current_admin_user
from app.api.schemas import (
    TransactionHistoryResponse,
    TransactionResponse,
    APIResponse
)
from app.models import User, TransactionType, TransactionStatus
from app.services.transaction_service import transaction_service


router = APIRouter()


@router.get("/history", response_model=TransactionHistoryResponse)
async def get_transaction_history(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    transaction_type: Optional[TransactionType] = Query(None, description="Filter by transaction type"),
    status: Optional[TransactionStatus] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_active_user)
):
    """Get user transaction history with pagination."""
    return await transaction_service.get_transaction_history(
        user_id=str(current_user.id),
        page=page,
        size=size,
        transaction_type=transaction_type,
        transaction_status=status
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get specific transaction by ID."""
    return await transaction_service.get_transaction_by_id(
        transaction_id=transaction_id,
        user_id=str(current_user.id)
    )


@router.get("/admin/recent", response_model=list[TransactionResponse])
async def get_recent_transactions(
    limit: int = Query(10, ge=1, le=50, description="Number of transactions to return"),
    current_user: User = Depends(get_current_admin_user)
):
    """Get recent transactions (Admin only)."""
    return await transaction_service.get_recent_transactions(limit=limit)
