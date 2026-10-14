import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.core.config import settings
from backend.app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health Check Endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "district": settings.DISTRICT_NAME,
        "node_cluster": settings.NODE_CLUSTER,
    }

# Mount Frontend Static Assets if available in parent directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CSS_DIR = ROOT_DIR / "css"
JS_DIR = ROOT_DIR / "js"
ASSETS_DIR = ROOT_DIR / "assets"

if CSS_DIR.exists():
    app.mount("/css", StaticFiles(directory=str(CSS_DIR)), name="css")
if JS_DIR.exists():
    app.mount("/js", StaticFiles(directory=str(JS_DIR)), name="js")
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

# Frontend Web Views Direct Routing
@app.get("/", tags=["Frontend Views"], include_in_schema=False)
def serve_index():
    index_file = ROOT_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": "/health",
        "api_v1": settings.API_V1_STR
    }

@app.get("/incident-intelligence.html", tags=["Frontend Views"], include_in_schema=False)
def serve_incident_intelligence():
    file_path = ROOT_DIR / "incident-intelligence.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return {"detail": "View not found"}

@app.get("/resolution-verification.html", tags=["Frontend Views"], include_in_schema=False)
def serve_resolution_verification():
    file_path = ROOT_DIR / "resolution-verification.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return {"detail": "View not found"}

@app.get("/public-transparency.html", tags=["Frontend Views"], include_in_schema=False)
def serve_public_transparency():
    file_path = ROOT_DIR / "public-transparency.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return {"detail": "View not found"}
