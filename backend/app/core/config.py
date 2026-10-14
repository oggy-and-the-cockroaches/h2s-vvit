from typing import List
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "CivicPulse AI Operations Platform API"
    VERSION: str = "4.8.2"
    DESCRIPTION: str = (
        "High-performance municipal operations backend providing autonomous AI triage, "
        "multimodal forensic evidence streaming, cryptographic resolution verification, "
        "and public civic transparency feeds."
    )
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["*"]
    DISTRICT_NAME: str = "Metro Central District 04"
    SECTOR: str = "Sector North"
    NODE_CLUSTER: str = "N-ALPHA-09"

settings = Settings()
