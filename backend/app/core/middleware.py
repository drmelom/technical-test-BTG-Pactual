import logging
import time
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("btg_pactual")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de requests y responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def setup_cors(app) -> None:
    """Configure CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React dev server
            "http://localhost:3001",  # Alternative port
            "http://localhost:8080",  # Vue/Angular dev server
            "https://btgpactual-frontend.vercel.app",  # Production frontend
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time"]
    )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware para añadir headers de seguridad."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("btg_pactual.log", encoding="utf-8")
        ]
    )
    
    # Configure specific loggers
    logging.getLogger("uvicorn.access").disabled = True  # Disable uvicorn access logs
    logging.getLogger("motor").setLevel(logging.WARNING)  # Reduce MongoDB logs
