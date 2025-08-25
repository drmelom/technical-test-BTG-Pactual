from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid

from beanie import PydanticObjectId

from app.models import Transaction, TransactionType, TransactionStatus


class TransactionRepository:
    """Repository for Transaction operations."""
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID."""
        return f"TXN_{datetime.utcnow().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8].upper()}"
    
    async def create(
        self,
        user_id: str,
        fund_id: int,
        transaction_type: TransactionType,
        amount: Decimal,
        description: Optional[str] = None
    ) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(
            transaction_id=self._generate_transaction_id(),
            user_id=user_id,
            fund_id=fund_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            status=TransactionStatus.PENDING
        )
        await transaction.insert()
        return transaction
    
    async def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by transaction_id."""
        return await Transaction.find_one(Transaction.transaction_id == transaction_id)
    
    async def get_by_object_id(self, object_id: str) -> Optional[Transaction]:
        """Get transaction by MongoDB object ID."""
        try:
            return await Transaction.get(PydanticObjectId(object_id))
        except Exception:
            return None
    
    async def update_status(
        self, 
        transaction_id: str, 
        status: TransactionStatus
    ) -> Optional[Transaction]:
        """Update transaction status."""
        transaction = await self.get_by_id(transaction_id)
        if not transaction:
            return None
        
        transaction.status = status
        transaction.updated_at = datetime.utcnow()
        
        if status == TransactionStatus.COMPLETED:
            transaction.completed_at = datetime.utcnow()
        
        await transaction.save()
        return transaction
    
    async def get_user_transactions(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        transaction_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None
    ) -> List[Transaction]:
        """Get user transactions with pagination and filters."""
        query = {"user_id": user_id}
        
        if transaction_type:
            query["transaction_type"] = transaction_type
        
        if status:
            query["status"] = status
        
        return await Transaction.find(query)\
            .sort(-Transaction.created_at)\
            .skip(skip)\
            .limit(limit)\
            .to_list()
    
    async def count_user_transactions(
        self,
        user_id: str,
        transaction_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None
    ) -> int:
        """Count user transactions with filters."""
        query = {"user_id": user_id}
        
        if transaction_type:
            query["transaction_type"] = transaction_type
        
        if status:
            query["status"] = status
        
        return await Transaction.find(query).count()
    
    async def get_fund_transactions(
        self,
        fund_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[Transaction]:
        """Get fund transactions with pagination."""
        return await Transaction.find(Transaction.fund_id == fund_id)\
            .sort(-Transaction.created_at)\
            .skip(skip)\
            .limit(limit)\
            .to_list()
    
    async def get_recent_transactions(
        self,
        limit: int = 10
    ) -> List[Transaction]:
        """Get recent transactions."""
        return await Transaction.find()\
            .sort(-Transaction.created_at)\
            .limit(limit)\
            .to_list()


# Create repository instance
transaction_repository = TransactionRepository()
