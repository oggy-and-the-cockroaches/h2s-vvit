"""
CivicPulse AI Operations Platform - Security Engine & Protection Middleware.

Provides:
- Strict HTTP Security Headers Middleware (CSP, HSTS, X-Frame-Options, etc.)
- In-memory Sliding Window Rate Limiting Middleware with 429 response
- Request Payload Size Limiting Middleware
- Input Sanitization (XSS prevention and HTML entity encoding)
"""

import html
import re
import time
from typing import Dict, List, Tuple
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from backend.app.core.config import settings


# ---------------------------------------------------------------------------
# 1. Input Sanitization Utilities
# ---------------------------------------------------------------------------

DANGEROUS_PATTERNS = [
    re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>", re.IGNORECASE | re.DOTALL),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"on\w+\s*=", re.IGNORECASE),
    re.compile(r"<\s*embed[^>]*>", re.IGNORECASE),
    re.compile(r"<\s*object[^>]*>", re.IGNORECASE),
]


def sanitize_input(text: str) -> str:
    """
    Sanitize untrusted user string inputs by removing active script tags,
    event handlers, and HTML encoding special characters.
    
    Args:
        text (str): Raw untrusted user input string.
        
    Returns:
        str: Sanitized, XSS-safe string.
    """
    if not isinstance(text, str):
        return text

    sanitized = text
    for pattern in DANGEROUS_PATTERNS:
        sanitized = pattern.sub("", sanitized)

    # Encode HTML entities to prevent DOM XSS injection
    sanitized = html.escape(sanitized, quote=True)
    return sanitized.strip()


# ---------------------------------------------------------------------------
# 2. Security Headers Middleware
# ---------------------------------------------------------------------------

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Injects enterprise-grade security headers on every HTTP response.
    Enforces Content-Security-Policy, HSTS, frame protection, and content type sniffing guards.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Content Security Policy (allows necessary CDNs for Fonts & Tailwind while blocking rogue execution)
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https: blob:",
            "connect-src 'self' ws: wss: http: https:",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # Anti-Clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # HTTP Strict Transport Security (HSTS - 1 year with subdomains)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (disable intrusive browser features)
        response.headers["Permissions-Policy"] = (
            "geolocation=(), camera=(), microphone=(), payment=(), usb=()"
        )

        # Cross-Site Scripting filter for legacy browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Cache control for sensitive API routes
        if request.url.path.startswith(settings.API_V1_STR):
            if "Cache-Control" not in response.headers:
                response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
                response.headers["Pragma"] = "no-cache"

        return response


# ---------------------------------------------------------------------------
# 3. Sliding Window Rate Limiter Middleware
# ---------------------------------------------------------------------------

class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Sliding window in-memory rate limiter per client IP address.
    Protects public APIs against Denial of Service (DoS) and brute force flooding.
    """

    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        # Maps client_ip -> list of timestamps
        self.clients: Dict[str, List[float]] = {}
        # Whitelisted internal endpoints exempt from aggressive throttling
        self.exempt_paths = {"/health", "/docs", "/redoc", f"{settings.API_V1_STR}/openapi.json"}

    def _cleanup_old_records(self, ip: str, current_time: float):
        cutoff = current_time - self.window_seconds
        if ip in self.clients:
            self.clients[ip] = [t for t in self.clients[ip] if t > cutoff]
            if not self.clients[ip]:
                del self.clients[ip]

    async def dispatch(self, request: Request, call_next) -> Response:
        # Check exemption
        if request.url.path in self.exempt_paths or request.url.path.endswith("/ws"):
            return await call_next(request)

        # Identify client
        client_ip = request.client.host if request.client else "127.0.0.1"
        current_time = time.time()

        self._cleanup_old_records(client_ip, current_time)

        client_history = self.clients.setdefault(client_ip, [])

        if len(client_history) >= self.requests_per_minute:
            retry_after = int(self.window_seconds - (current_time - client_history[0]))
            retry_after = max(1, retry_after)
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.",
                    "retry_after_seconds": retry_after
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                }
            )

        # Record this request
        client_history.append(current_time)
        remaining = self.requests_per_minute - len(client_history)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response


# ---------------------------------------------------------------------------
# 4. Request Payload Size Limiting Middleware
# ---------------------------------------------------------------------------

class RequestSizeLimiterMiddleware(BaseHTTPMiddleware):
    """
    Limits the maximum incoming request payload size (e.g. 2 MB)
    to protect against memory exhaustion attacks.
    """

    def __init__(self, app, max_upload_size: int = 2 * 1024 * 1024):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next) -> Response:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_upload_size:
            return JSONResponse(
                status_code=413,
                content={
                    "error": "Payload Too Large",
                    "detail": f"Request body exceeds maximum allowed size of {self.max_upload_size} bytes."
                }
            )
        return await call_next(request)
