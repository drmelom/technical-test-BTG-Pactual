from typing import List, Optional
from decimal import Decimal

from fastapi import HTTPException, status

from app.models import Transaction, TransactionType, TransactionStatus
from app.repositories.transaction_repository import transaction_repository
from app.repositories.user_repository import user_repository


class TransactionService:
    """Service for transaction operations."""
    
    async def get_transaction_history(
        self,
        user_id: str,
        page: int = 1,
        size: int = 10,
        transaction_type: Optional[TransactionType] = None,
        transaction_status: Optional[TransactionStatus] = None
    ) -> dict:
        """Get user transaction history with pagination."""
        # Validate user exists
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Calculate pagination
        skip = (page - 1) * size
        
        # Get transactions
        transactions = await transaction_repository.get_user_transactions(
            user_id=user_id,
            skip=skip,
            limit=size,
            transaction_type=transaction_type,
            status=transaction_status
        )
        
        # Get total count
        total = await transaction_repository.count_user_transactions(
            user_id=user_id,
            transaction_type=transaction_type,
            status=transaction_status
        )
        
        # Calculate pages
        pages = (total + size - 1) // size
        
        return {
            "transactions": transactions,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }
    
    async def get_transaction_by_id(
        self,
        transaction_id: str,
        user_id: Optional[str] = None
    ) -> Transaction:
        """Get transaction by ID."""
        transaction = await transaction_repository.get_by_id(transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # If user_id provided, verify ownership
        if user_id and transaction.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this transaction"
            )
        
        return transaction
    
    async def get_recent_transactions(self, limit: int = 10) -> List[Transaction]:
        """Get recent transactions (admin only)."""
        return await transaction_repository.get_recent_transactions(limit=limit)


# Create service instance
transaction_service = TransactionService()
