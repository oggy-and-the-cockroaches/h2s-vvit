"""
CivicPulse AI Operations Platform - Application Configuration & Settings.
"""

from typing import List
from pydantic import BaseModel, Field


class Settings(BaseModel):
    PROJECT_NAME: str = "CivicPulse AI Operations Platform API"
    VERSION: str = "4.8.2"
    DESCRIPTION: str = (
        "High-performance municipal operations backend providing autonomous AI triage, "
        "multimodal forensic evidence streaming, cryptographic resolution verification, "
        "and public civic transparency feeds."
    )
    API_V1_STR: str = "/api/v1"
    
    # Security Configuration
    CORS_ORIGINS: List[str] = Field(
        default=[
            "https://ajayhemanth.online",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:3000",
            "http://127.0.0.1:5500",
            "*"
        ],
        description="Allowed origins for CORS requests."
    )
    RATE_LIMIT_PER_MINUTE: int = Field(default=120, description="Max requests per minute per IP")
    MAX_REQUEST_SIZE_BYTES: int = Field(default=2 * 1024 * 1024, description="Max upload size (2MB)")
    ENABLE_SECURITY_HEADERS: bool = True
    ENABLE_GZIP_COMPRESSION: bool = True
    GZIP_MINIMUM_SIZE: int = 500  # bytes
    
    # Operations Metadata
    DISTRICT_NAME: str = "Metro Central District 04"
    SECTOR: str = "Sector North"
    NODE_CLUSTER: str = "N-ALPHA-09"
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"


settings = Settings()
