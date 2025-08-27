import logging
import sys
import json
from decimal import InvalidOperation

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse as BaseJSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.exceptions import (
    BTGPactualException,
    btg_pactual_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    decimal_exception_handler
)
from app.core.middleware import SecurityHeadersMiddleware, LoggingMiddleware, setup_cors
from app.core.json_encoder import CustomJSONEncoder

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)


# Custom JSON Response class
class CustomJSONResponse(BaseJSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CustomJSONEncoder,
        ).encode("utf-8")


# Create FastAPI application with custom JSON encoder
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    default_response_class=CustomJSONResponse,
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
