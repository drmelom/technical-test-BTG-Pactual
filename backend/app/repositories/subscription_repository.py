from typing import List, Optional
from datetime import datetime

from beanie import PydanticObjectId

from app.models import UserFundSubscription
from app.repositories.fund_repository import fund_repository


class SubscriptionRepository:
    """Repository for UserFundSubscription operations."""
    
    async def create(
        self,
        user_id: str,
        fund_id: int,
        subscription_amount: float
    ) -> UserFundSubscription:
        """Create a new subscription."""
        subscription = UserFundSubscription(
            user_id=user_id,
            fund_id=fund_id,
            subscription_amount=subscription_amount,
            is_active=True
        )
        await subscription.insert()
        return subscription
    
    async def get_by_user_and_fund(
        self, 
        user_id: str, 
        fund_id: int
    ) -> Optional[UserFundSubscription]:
        """Get subscription by user and fund."""
        return await UserFundSubscription.find_one(
            UserFundSubscription.user_id == user_id,
            UserFundSubscription.fund_id == fund_id,
            UserFundSubscription.is_active == True
        )
    
    async def get_user_subscriptions(
        self, 
        user_id: str,
        is_active: Optional[bool] = True
    ) -> List[dict]:
        """Get user subscriptions with fund details."""
        query = {"user_id": user_id}
        if is_active is not None:
            query["is_active"] = is_active
        
        subscriptions = await UserFundSubscription.find(query).to_list()
        
        # Enrich with fund data
        result = []
        for subscription in subscriptions:
            fund = await fund_repository.get_by_id(subscription.fund_id)
            if fund:
                result.append({
                    "id": str(subscription.id),
                    "user_id": subscription.user_id,
                    "fund_id": subscription.fund_id,
                    "fund_name": fund.name,
                    "subscription_amount": subscription.subscription_amount,
                    "is_active": subscription.is_active,
                    "subscribed_at": subscription.subscribed_at,
                    "cancelled_at": subscription.cancelled_at
                })
        
        return result
    
    async def cancel_subscription(
        self, 
        user_id: str, 
        fund_id: int
    ) -> Optional[UserFundSubscription]:
        """Cancel user subscription to fund."""
        subscription = await self.get_by_user_and_fund(user_id, fund_id)
        if not subscription:
            return None
        
        subscription.is_active = False
        subscription.cancelled_at = datetime.utcnow()
        await subscription.save()
        return subscription
    
    async def get_fund_subscriptions(
        self, 
        fund_id: int,
        is_active: Optional[bool] = True
    ) -> List[UserFundSubscription]:
        """Get all subscriptions for a fund."""
        query = {"fund_id": fund_id}
        if is_active is not None:
            query["is_active"] = is_active
        
        return await UserFundSubscription.find(query).to_list()
    
    async def count_fund_subscriptions(
        self, 
        fund_id: int,
        is_active: Optional[bool] = True
    ) -> int:
        """Count subscriptions for a fund."""
        query = {"fund_id": fund_id}
        if is_active is not None:
            query["is_active"] = is_active
        
        return await UserFundSubscription.find(query).count()


# Create repository instance
subscription_repository = SubscriptionRepository()
