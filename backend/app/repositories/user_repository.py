from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from app.models import User, UserRole
from app.core.security import security


class UserRepository:
    """Repository for User operations."""
    
    async def create(
        self, 
        email: str, 
        password: str, 
        full_name: str,
        phone_number: Optional[str] = None,
        notification_preference: str = "email"
    ) -> User:
        """Create a new user."""
        try:
            hashed_password = security.get_password_hash(password)
            user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                phone_number=phone_number,
                notification_preference=notification_preference,
                role=UserRole.CLIENT,
                current_balance=Decimal("500000")  # Initial balance COP $500.000
            )
            await user.insert()
            return user
        except DuplicateKeyError:
            raise ValueError(f"User with email {email} already exists")
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return await User.find_one(User.email == email)
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            return await User.get(PydanticObjectId(user_id))
        except Exception:
            return None
    
    async def update(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user."""
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        await user.save()
        return user
    
    async def update_balance(self, user_id: str, new_balance: Decimal) -> Optional[User]:
        """Update user balance."""
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        user.current_balance = new_balance
        user.updated_at = datetime.utcnow()
        await user.save()
        return user
    
    async def deactivate(self, user_id: str) -> Optional[User]:
        """Deactivate user."""
        return await self.update(user_id, is_active=False)
    
    async def activate(self, user_id: str) -> Optional[User]:
        """Activate user."""
        return await self.update(user_id, is_active=True)
    
    async def list_users(
        self, 
        skip: int = 0, 
        limit: int = 10,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """List users with pagination."""
        query = {}
        if is_active is not None:
            query["is_active"] = is_active
            
        return await User.find(query).skip(skip).limit(limit).to_list()
    
    async def count_users(self, is_active: Optional[bool] = None) -> int:
        """Count users."""
        query = {}
        if is_active is not None:
            query["is_active"] = is_active
            
        return await User.find(query).count()
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        user = await self.get_by_email(email)
        if not user:
            return None
        
        if not security.verify_password(password, user.hashed_password):
            return None
        
        return user


# Create repository instance
user_repository = UserRepository()
