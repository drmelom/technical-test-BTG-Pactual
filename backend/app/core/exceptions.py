from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
import logging
from decimal import InvalidOperation

logger = logging.getLogger(__name__)


class BTGPactualException(Exception):
    """Base exception for BTG Pactual application."""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class InsufficientFundsException(BTGPactualException):
    """Exception raised when user has insufficient funds."""
    
    def __init__(self, message: str = "Saldo insuficiente para realizar la operación"):
        super().__init__(message, "INSUFFICIENT_FUNDS")


class FundNotFoundException(BTGPactualException):
    """Exception raised when fund is not found."""
    
    def __init__(self, message: str = "Fondo no encontrado"):
        super().__init__(message, "FUND_NOT_FOUND")


class UserNotFoundException(BTGPactualException):
    """Exception raised when user is not found."""
    
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message, "USER_NOT_FOUND")


class SubscriptionNotFoundException(BTGPactualException):
    """Exception raised when subscription is not found."""
    
    def __init__(self, message: str = "Suscripción no encontrada"):
        super().__init__(message, "SUBSCRIPTION_NOT_FOUND")


class AlreadySubscribedException(BTGPactualException):
    """Exception raised when user is already subscribed to a fund."""
    
    def __init__(self, message: str = "Ya estás suscrito a este fondo"):
        super().__init__(message, "ALREADY_SUBSCRIBED")


class TransactionException(BTGPactualException):
    """Exception raised during transaction processing."""
    
    def __init__(self, message: str = "Error procesando la transacción"):
        super().__init__(message, "TRANSACTION_ERROR")


class NotificationException(BTGPactualException):
    """Exception raised during notification sending."""
    
    def __init__(self, message: str = "Error enviando notificación"):
        super().__init__(message, "NOTIFICATION_ERROR")


async def btg_pactual_exception_handler(request: Request, exc: BTGPactualException):
    """Handle custom BTG Pactual exceptions."""
    logger.error(f"BTGPactualException: {exc.message} (code: {exc.error_code})")
    
    status_code = 400
    if isinstance(exc, (UserNotFoundException, FundNotFoundException, SubscriptionNotFoundException)):
        status_code = 404
    elif isinstance(exc, (InsufficientFundsException, AlreadySubscribedException)):
        status_code = 400
    elif isinstance(exc, (TransactionException, NotificationException)):
        status_code = 500
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": True,
            "message": exc.message,
            "error_code": exc.error_code,
            "detail": None
        }
    )


async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]):
    """Handle HTTP exceptions."""
    logger.error(f"HTTPException: {exc.detail} (status: {exc.status_code})")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "detail": None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(f"ValidationError: {exc.errors()}")
    
    # Format validation errors
    errors = []
    for error in exc.errors():
        location = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": location,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Error de validación en los datos enviados",
            "error_code": "VALIDATION_ERROR",
            "detail": errors
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    # Don't expose internal errors in production
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "error_code": "INTERNAL_ERROR",
            "detail": None
        }
    )


async def decimal_exception_handler(request: Request, exc: InvalidOperation):
    """Handle decimal operation errors."""
    logger.error(f"Decimal operation error: {str(exc)}")
    
    return JSONResponse(
        status_code=400,
        content={
            "error": True,
            "message": "Error en el formato de cantidad monetaria",
            "error_code": "INVALID_DECIMAL",
            "detail": None
        }
    )
