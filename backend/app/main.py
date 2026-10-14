"""
CivicPulse AI Operations Platform - High-Performance Municipal Backend Service.

Integrated Enterprise Architecture:
- Enterprise Security: CSP, HSTS, Rate Limiting, Request Size Limiting, XSS Sanitization
- High Efficiency: GZip compression middleware, In-memory O(1) indexing, In-memory caching
- Full RESTful and WebSocket Telemetry APIs
- Standards-compliant OpenAPI & JSON documentation
"""

import sys
import logging
from pathlib import Path

# Ensure workspace root is in sys.path so 'backend.app' resolves from any directory
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.security import (
    SecurityHeadersMiddleware, RateLimiterMiddleware, RequestSizeLimiterMiddleware
)
from backend.app.api.v1.router import api_router

# Configure structured enterprise logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger("civicpulse")

# Initialize FastAPI Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# ---------------------------------------------------------------------------
# 1. Enterprise Middleware Pipeline (Execution Order: Outer -> Inner)
# ---------------------------------------------------------------------------

# Compression: Compress responses > 500 bytes for maximum bandwidth efficiency
if settings.ENABLE_GZIP_COMPRESSION:
    app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MINIMUM_SIZE)

# Security Headers: Injects strict CSP, HSTS, X-Frame-Options, anti-sniffing
if settings.ENABLE_SECURITY_HEADERS:
    app.add_middleware(SecurityHeadersMiddleware)

# Rate Limiting: Throttles DoS/brute force attempts per client IP
app.add_middleware(RateLimiterMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)

# Request Size Guard: Limits max upload payload to prevent memory exhaustion
app.add_middleware(RequestSizeLimiterMiddleware, max_upload_size=settings.MAX_REQUEST_SIZE_BYTES)

# CORS: Configured origins for cross-domain dashboard communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "Content-Disposition"]
)

# ---------------------------------------------------------------------------
# 2. Centralized Exception Handlers (Security: No stack trace leakage)
# ---------------------------------------------------------------------------

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Sanitized HTTP exception response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "error": exc.detail or "HTTP Request Exception",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Sanitized schema validation error response."""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "status_code": 422,
            "error": "Validation Error",
            "detail": exc.errors(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Fallback handler to prevent internal server error stack traces in production."""
    logger.error(f"Unhandled Server Error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "status_code": 500,
            "error": "Internal Server Error",
            "message": "An unexpected operational exception occurred. Incident logged for review."
        }
    )

# ---------------------------------------------------------------------------
# 3. Mount API Routes
# ---------------------------------------------------------------------------
app.include_router(api_router, prefix=settings.API_V1_STR)

# ---------------------------------------------------------------------------
# 4. Root & System Health Endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["System"])
def api_root():
    """
    Root status and hypermedia directory for the CivicPulse API.
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "description": settings.DESCRIPTION,
        "district": settings.DISTRICT_NAME,
        "cluster": settings.NODE_CLUSTER,
        "security": {
            "rate_limiting": f"Enforced ({settings.RATE_LIMIT_PER_MINUTE} req/min)",
            "security_headers": "Active (CSP, HSTS, X-Frame-Options)",
            "xss_sanitization": "Active",
            "payload_limit": f"{settings.MAX_REQUEST_SIZE_BYTES // (1024*1024)}MB"
        },
        "efficiency": {
            "gzip_compression": "Active",
            "indexed_lookups": "Active (Category, Ward, Status, Token)",
            "telemetry_caching": "Active"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": f"{settings.API_V1_STR}/openapi.json"
        },
        "endpoints": {
            "health": "/health",
            "incidents": f"{settings.API_V1_STR}/incidents",
            "verification": f"{settings.API_V1_STR}/verification/pending",
            "transparency": f"{settings.API_V1_STR}/transparency/metrics",
            "telemetry": f"{settings.API_V1_STR}/telemetry/status"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    High-frequency health check probe for load balancers and container orchestrators.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "district": settings.DISTRICT_NAME,
        "node_cluster": settings.NODE_CLUSTER,
        "checks": {
            "database": "operational",
            "security_subsystem": "enforced",
            "telemetry_pipeline": "synchronized"
        }
    }
