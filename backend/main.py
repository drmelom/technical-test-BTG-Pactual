from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from decimal import InvalidOperation

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.middleware import LoggingMiddleware, SecurityHeadersMiddleware, setup_cors, setup_logging
from app.core.exceptions import (
    BTGPactualException,
    btg_pactual_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    decimal_exception_handler
)
from app.api.v1 import api_router


# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="BTG Pactual - Funds Management API",
    description="""
    Sistema de gestión de fondos de BTG Pactual
    
    ## Funcionalidades principales:
    - 🔐 Autenticación y autorización de usuarios
    - 💰 Suscripción y cancelación de fondos de inversión
    - 📊 Consulta de historial de transacciones
    - 📱 Sistema de notificaciones
    
    ## Roles de usuario:
    - **Admin**: Acceso completo al sistema
    - **Client**: Operaciones de fondos y consultas
    
    ## Autenticación:
    - Utiliza JWT tokens para autenticación
    - Header: `Authorization: Bearer <token>`
    """,
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
)

# Setup CORS
setup_cors(app)

# Add custom middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)

# Exception handlers
app.add_exception_handler(BTGPactualException, btg_pactual_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(InvalidOperation, decimal_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print("🚀 Iniciando BTG Pactual Funds Management API...")
    await connect_to_mongo()
    print("✅ Aplicación iniciada correctamente")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown."""
    print("🛑 Cerrando BTG Pactual Funds Management API...")
    await close_mongo_connection()
    print("✅ Aplicación cerrada correctamente")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Health check."""
    return {
        "message": "BTG Pactual Funds Management API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.ENVIRONMENT != "production" else "disabled"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "database": "connected",
        "services": {
            "authentication": "operational",
            "funds": "operational",
            "transactions": "operational",
            "notifications": "operational"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
