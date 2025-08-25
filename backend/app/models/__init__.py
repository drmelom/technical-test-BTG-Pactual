from datetime import datetime
from enum import Enum
from typing import List, Optional
from decimal import Decimal

from beanie import Document, Indexed
from pydantic import BaseModel, Field, validator
from pymongo import IndexModel, ASCENDING, DESCENDING


class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"


class NotificationPreference(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"


class FundCategory(str, Enum):
    FPV = "FPV"
    FIC = "FIC"


class TransactionType(str, Enum):
    SUBSCRIPTION = "subscription"
    CANCELLATION = "cancellation"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Document):
    """User model for authentication and client management"""
    
    email: Indexed(str, unique=True) = Field(..., description="User email")
    hashed_password: str = Field(..., description="Hashed password")
    full_name: str = Field(..., description="User full name")
    phone: Optional[str] = Field(None, description="User phone number")
    role: UserRole = Field(default=UserRole.CLIENT, description="User role")
    is_active: bool = Field(default=True, description="User active status")
    notification_preference: NotificationPreference = Field(
        default=NotificationPreference.EMAIL,
        description="Notification preference"
    )
    current_balance: Decimal = Field(
        default=Decimal("500000"),
        description="Current balance in COP"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("created_at", DESCENDING)]),
        ]

    @validator("current_balance", pre=True)
    def validate_balance(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v


class Fund(Document):
    """Fund model representing investment funds"""
    
    fund_id: Indexed(int, unique=True) = Field(..., description="Fund ID")
    name: str = Field(..., description="Fund name")
    minimum_amount: Decimal = Field(..., description="Minimum subscription amount in COP")
    category: FundCategory = Field(..., description="Fund category")
    description: Optional[str] = Field(None, description="Fund description")
    is_active: bool = Field(default=True, description="Fund active status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "funds"
        indexes = [
            IndexModel([("fund_id", ASCENDING)], unique=True),
            IndexModel([("category", ASCENDING)]),
            IndexModel([("is_active", ASCENDING)]),
        ]

    @validator("minimum_amount", pre=True)
    def validate_minimum_amount(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v


class Transaction(Document):
    """Transaction model for fund subscriptions and cancellations"""
    
    transaction_id: Indexed(str, unique=True) = Field(..., description="Unique transaction ID")
    user_id: Indexed(str) = Field(..., description="User ID who made the transaction")
    fund_id: int = Field(..., description="Fund ID")
    transaction_type: TransactionType = Field(..., description="Transaction type")
    amount: Decimal = Field(..., description="Transaction amount in COP")
    status: TransactionStatus = Field(
        default=TransactionStatus.PENDING,
        description="Transaction status"
    )
    description: Optional[str] = Field(None, description="Transaction description")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(None, description="Transaction completion time")

    class Settings:
        name = "transactions"
        indexes = [
            IndexModel([("transaction_id", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("fund_id", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("user_id", ASCENDING), ("created_at", DESCENDING)]),
        ]

    @validator("amount", pre=True)
    def validate_amount(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v


class UserFundSubscription(Document):
    """Model to track user subscriptions to funds"""
    
    user_id: Indexed(str) = Field(..., description="User ID")
    fund_id: Indexed(int) = Field(..., description="Fund ID")
    subscription_amount: Decimal = Field(..., description="Current subscription amount")
    is_active: bool = Field(default=True, description="Subscription status")
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    cancelled_at: Optional[datetime] = Field(None, description="Cancellation date")

    class Settings:
        name = "user_fund_subscriptions"
        indexes = [
            IndexModel([("user_id", ASCENDING), ("fund_id", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("fund_id", ASCENDING)]),
            IndexModel([("is_active", ASCENDING)]),
        ]

    @validator("subscription_amount", pre=True)
    def validate_subscription_amount(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v


# Initialize default funds data
DEFAULT_FUNDS = [
    {
        "fund_id": 1,
        "name": "FPV_BTG_PACTUAL_RECAUDADORA",
        "minimum_amount": Decimal("75000"),
        "category": FundCategory.FPV,
        "description": "Fondo de Pensiones Voluntarias BTG Pactual Recaudadora",
    },
    {
        "fund_id": 2,
        "name": "FPV_BTG_PACTUAL_ECOPETROL",
        "minimum_amount": Decimal("125000"),
        "category": FundCategory.FPV,
        "description": "Fondo de Pensiones Voluntarias BTG Pactual Ecopetrol",
    },
    {
        "fund_id": 3,
        "name": "DEUDAPRIVADA",
        "minimum_amount": Decimal("50000"),
        "category": FundCategory.FIC,
        "description": "Fondo de Inversión Colectiva de Deuda Privada",
    },
    {
        "fund_id": 4,
        "name": "FDO-ACCIONES",
        "minimum_amount": Decimal("250000"),
        "category": FundCategory.FIC,
        "description": "Fondo de Inversión Colectiva de Acciones",
    },
    {
        "fund_id": 5,
        "name": "FPV_BTG_PACTUAL_DINAMICA",
        "minimum_amount": Decimal("100000"),
        "category": FundCategory.FPV,
        "description": "Fondo de Pensiones Voluntarias BTG Pactual Dinámica",
    },
]
