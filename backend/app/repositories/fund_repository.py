from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from beanie import PydanticObjectId

from app.models import Fund, DEFAULT_FUNDS


class FundRepository:
    """Repository for Fund operations."""
    
    async def initialize_funds(self):
        """Initialize default funds if they don't exist."""
        existing_funds = await Fund.find_all().to_list()
        if not existing_funds:
            for fund_data in DEFAULT_FUNDS:
                fund = Fund(**fund_data)
                await fund.insert()
    
    async def get_all(self, is_active: Optional[bool] = True) -> List[Fund]:
        """Get all funds."""
        query = {}
        if is_active is not None:
            query["is_active"] = is_active
        
        return await Fund.find(query).to_list()
    
    async def get_by_id(self, fund_id: int) -> Optional[Fund]:
        """Get fund by fund_id."""
        return await Fund.find_one(Fund.fund_id == fund_id)
    
    async def get_by_object_id(self, object_id: str) -> Optional[Fund]:
        """Get fund by MongoDB object ID."""
        try:
            return await Fund.get(PydanticObjectId(object_id))
        except Exception:
            return None
    
    async def create(
        self, 
        fund_id: int,
        name: str,
        minimum_amount: Decimal,
        category: str,
        description: Optional[str] = None
    ) -> Fund:
        """Create a new fund."""
        fund = Fund(
            fund_id=fund_id,
            name=name,
            minimum_amount=minimum_amount,
            category=category,
            description=description
        )
        await fund.insert()
        return fund
    
    async def update(
        self, 
        fund_id: int, 
        **kwargs
    ) -> Optional[Fund]:
        """Update fund."""
        fund = await self.get_by_id(fund_id)
        if not fund:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(fund, key) and value is not None:
                setattr(fund, key, value)
        
        fund.updated_at = datetime.utcnow()
        await fund.save()
        return fund
    
    async def deactivate(self, fund_id: int) -> Optional[Fund]:
        """Deactivate fund."""
        return await self.update(fund_id, is_active=False)
    
    async def activate(self, fund_id: int) -> Optional[Fund]:
        """Activate fund."""
        return await self.update(fund_id, is_active=True)
    
    async def get_by_category(self, category: str) -> List[Fund]:
        """Get funds by category."""
        return await Fund.find(
            Fund.category == category, 
            Fund.is_active == True
        ).to_list()


# Create repository instance
fund_repository = FundRepository()
