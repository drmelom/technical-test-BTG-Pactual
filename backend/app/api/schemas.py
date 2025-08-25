from datetime import datetime
from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr, validator

from app.models import (
    UserRole, 
    NotificationPreference, 
    FundCategory, 
    TransactionType, 
    TransactionStatus
)


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = None
    notification_preference: NotificationPreference = NotificationPreference.EMAIL

    @validator("phone")
    def validate_phone(cls, v):
        if v is not None:
            import re
            if not re.match(r'^\+?[1-9]\d{1,14}$', v):
                raise ValueError("Invalid phone number format")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = None
    notification_preference: Optional[NotificationPreference] = None

    @validator("phone")
    def validate_phone(cls, v):
        if v is not None:
            import re
            if not re.match(r'^\+?[1-9]\d{1,14}$', v):
                raise ValueError("Invalid phone number format")
        return v


class UserResponse(UserBase):
    id: str = Field(..., alias="_id")
    role: UserRole
    is_active: bool
    current_balance: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None


# Fund Schemas
class FundBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    minimum_amount: Decimal = Field(..., gt=0)
    category: FundCategory
    description: Optional[str] = Field(None, max_length=500)


class FundCreate(FundBase):
    fund_id: int = Field(..., gt=0)


class FundUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    minimum_amount: Optional[Decimal] = Field(None, gt=0)
    category: Optional[FundCategory] = None
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class FundResponse(FundBase):
    id: str = Field(..., alias="_id")
    fund_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


# Transaction Schemas
class TransactionBase(BaseModel):
    fund_id: int = Field(..., gt=0)
    transaction_type: TransactionType


class SubscriptionRequest(TransactionBase):
    amount: Decimal = Field(..., gt=0)
    transaction_type: TransactionType = TransactionType.SUBSCRIPTION


class CancellationRequest(BaseModel):
    fund_id: int = Field(..., gt=0)
    transaction_type: TransactionType = TransactionType.CANCELLATION


class TransactionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    transaction_id: str
    user_id: str
    fund_id: int
    transaction_type: TransactionType
    amount: Decimal
    status: TransactionStatus
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class TransactionHistoryResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    size: int
    pages: int


# User Fund Subscription Schemas
class UserFundSubscriptionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    fund_id: int
    fund_name: str
    subscription_amount: Decimal
    is_active: bool
    subscribed_at: datetime
    cancelled_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True


# API Response Schemas
class APIResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None


# Balance Schema
class BalanceResponse(BaseModel):
    current_balance: Decimal
    currency: str = "COP"


# Notification Schema
class NotificationRequest(BaseModel):
    recipient: str
    message: str
    notification_type: NotificationPreference
