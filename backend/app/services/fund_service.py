from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from fastapi import HTTPException, status

from app.models import Fund, Transaction, TransactionType, TransactionStatus, User
from app.repositories.fund_repository import fund_repository
from app.repositories.user_repository import user_repository
from app.repositories.transaction_repository import transaction_repository
from app.repositories.subscription_repository import subscription_repository
from app.services.notification_service import notification_service


class FundService:
    """Service for fund operations."""
    
    async def get_all_funds(self, is_active: Optional[bool] = True) -> List[Fund]:
        """Get all funds."""
        funds = await fund_repository.get_all(is_active=is_active)
        return funds
    
    async def get_fund_by_id(self, fund_id: int) -> Fund:
        """Get fund by ID."""
        fund = await fund_repository.get_by_id(fund_id)
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
        return fund
    
    async def subscribe_to_fund(
        self, 
        user_id: str, 
        fund_id: int, 
        amount: Decimal
    ) -> dict:
        """Subscribe user to a fund."""
        # Get user and fund
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        fund = await fund_repository.get_by_id(fund_id)
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
        
        if not fund.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fund is not active"
            )
        
        # Validate minimum amount
        if amount < fund.minimum_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum subscription amount is COP ${fund.minimum_amount:,.0f}"
            )
        
        # Check if user has sufficient balance
        if user.current_balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No tiene saldo disponible para vincularse al fondo {fund.name}"
            )
        
        # Check if user already subscribed to this fund
        existing_subscription = await subscription_repository.get_by_user_and_fund(
            user_id, fund_id
        )
        if existing_subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already subscribed to this fund"
            )
        
        try:
            # Create transaction
            transaction = await transaction_repository.create(
                user_id=user_id,
                fund_id=fund_id,
                transaction_type=TransactionType.SUBSCRIPTION,
                amount=amount,
                description=f"Subscription to fund {fund.name}"
            )
            
            # Update user balance
            new_balance = user.current_balance - amount
            await user_repository.update_balance(user_id, new_balance)
            
            # Create subscription
            await subscription_repository.create(
                user_id=user_id,
                fund_id=fund_id,
                subscription_amount=amount
            )
            
            # Update transaction status to completed
            await transaction_repository.update_status(
                transaction.transaction_id,
                TransactionStatus.COMPLETED
            )
            
            # Send notification
            await notification_service.send_subscription_notification(
                user=user,
                fund=fund,
                amount=amount
            )
            
            return {
                "success": True,
                "message": f"Successfully subscribed to fund {fund.name}",
                "transaction_id": transaction.transaction_id,
                "amount": amount,
                "new_balance": new_balance
            }
            
        except Exception as e:
            # If anything fails, mark transaction as failed
            if 'transaction' in locals():
                await transaction_repository.update_status(
                    transaction.transaction_id,
                    TransactionStatus.FAILED
                )
            
            # Log the actual error for debugging
            print(f"Error in subscribe_to_fund: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process subscription: {str(e)}"
            )
    
    async def cancel_subscription(self, user_id: str, fund_id: int) -> dict:
        """Cancel user subscription to a fund."""
        # Get user and fund
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        fund = await fund_repository.get_by_id(fund_id)
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found"
            )
        
        # Check if user has active subscription
        subscription = await subscription_repository.get_by_user_and_fund(
            user_id, fund_id
        )
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active subscription found for this fund"
            )
        
        try:
            # Create cancellation transaction
            transaction = await transaction_repository.create(
                user_id=user_id,
                fund_id=fund_id,
                transaction_type=TransactionType.CANCELLATION,
                amount=subscription.subscription_amount,
                description=f"Cancellation of subscription to fund {fund.name}"
            )
            
            # Return money to user balance
            new_balance = user.current_balance + subscription.subscription_amount
            await user_repository.update_balance(user_id, new_balance)
            
            # Cancel subscription
            await subscription_repository.cancel_subscription(user_id, fund_id)
            
            # Update transaction status to completed
            await transaction_repository.update_status(
                transaction.transaction_id,
                TransactionStatus.COMPLETED
            )
            
            # Send notification
            await notification_service.send_cancellation_notification(
                user=user,
                fund=fund,
                amount=subscription.subscription_amount
            )
            
            return {
                "success": True,
                "message": f"Successfully cancelled subscription to fund {fund.name}",
                "transaction_id": transaction.transaction_id,
                "refunded_amount": subscription.subscription_amount,
                "new_balance": new_balance
            }
            
        except Exception as e:
            # If anything fails, mark transaction as failed
            if 'transaction' in locals():
                await transaction_repository.update_status(
                    transaction.transaction_id,
                    TransactionStatus.FAILED
                )
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process cancellation"
            )
    
    async def get_user_subscriptions(self, user_id: str) -> List[dict]:
        """Get user active subscriptions."""
        subscriptions = await subscription_repository.get_user_subscriptions(
            user_id, is_active=True
        )
        return subscriptions


# Create service instance
fund_service = FundService()
