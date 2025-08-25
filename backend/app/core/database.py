import asyncio
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models import User, Fund, Transaction, UserFundSubscription, DEFAULT_FUNDS


class Database:
    client: Optional[AsyncIOMotorClient] = None


db = Database()


async def connect_to_mongo():
    """Create database connection."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Initialize beanie with the database
    await init_beanie(
        database=db.client[settings.DATABASE_NAME],
        document_models=[User, Fund, Transaction, UserFundSubscription]
    )
    
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")
    
    # Initialize default funds
    await initialize_default_data()


async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")


async def initialize_default_data():
    """Initialize default data (funds, admin user, etc.)."""
    try:
        # Initialize default funds
        existing_funds = await Fund.find_all().to_list()
        if not existing_funds:
            print("Initializing default funds...")
            for fund_data in DEFAULT_FUNDS:
                fund = Fund(**fund_data)
                await fund.insert()
            print("Default funds created successfully")
        
        # Create default admin user if it doesn't exist
        admin_email = "admin@btgpactual.com"
        existing_admin = await User.find_one(User.email == admin_email)
        
        if not existing_admin:
            print("Creating default admin user...")
            from app.core.security import security
            from app.models import UserRole, NotificationPreference
            from decimal import Decimal
            
            admin_user = User(
                email=admin_email,
                hashed_password=security.get_password_hash("Admin123!"),
                full_name="BTG Pactual Administrator",
                role=UserRole.ADMIN,
                is_active=True,
                notification_preference=NotificationPreference.EMAIL,
                current_balance=Decimal("1000000")  # COP $1.000.000 for admin
            )
            await admin_user.insert()
            print(f"Default admin user created: {admin_email}")
            print("Default admin password: Admin123!")
        
    except Exception as e:
        print(f"Error initializing default data: {str(e)}")


async def get_database():
    """Get database instance."""
    return db.client[settings.DATABASE_NAME] if db.client else None
