from fastapi import APIRouter

from app.api.v1 import auth, users, funds, transactions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(funds.router, prefix="/funds", tags=["Funds"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
