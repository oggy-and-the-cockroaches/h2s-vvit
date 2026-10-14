from fastapi import APIRouter
from backend.app.api.v1.endpoints.incidents import router as incidents_router
from backend.app.api.v1.endpoints.verification import router as verification_router
from backend.app.api.v1.endpoints.transparency import router as transparency_router
from backend.app.api.v1.endpoints.telemetry import router as telemetry_router

api_router = APIRouter()
api_router.include_router(incidents_router)
api_router.include_router(verification_router)
api_router.include_router(transparency_router)
api_router.include_router(telemetry_router)
