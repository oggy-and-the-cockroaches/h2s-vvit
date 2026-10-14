"""
CivicPulse AI Operations Platform - Incident Management & Triage Endpoints.

Handles real-time incident queue, single-dossier queries, citizen report ingestion,
and operational procedure checklist updates.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.models.schemas import Incident, IncidentCreate
from backend.app.data.database import db

router = APIRouter(prefix="/incidents", tags=["Incidents & Triage"])


@router.get("", response_model=List[Incident], summary="List and filter municipal incidents")
def list_incidents(
    category: Optional[str] = Query(None, description="Filter by category (e.g. Electrical Hazards, Roadways & Drainage)"),
    ward: Optional[str] = Query(None, description="Filter by ward (e.g. Ward 4)"),
    status: Optional[str] = Query(None, description="Filter by status (e.g. Dispatched, Awaiting Verification)"),
    min_priority: Optional[int] = Query(None, ge=0, le=100, description="Minimum priority score"),
    search: Optional[str] = Query(None, min_length=1, max_length=100, description="Search keyword in ID, title, or address")
):
    """
    Retrieve real-time municipal incident queue ranked by AI priority score.
    Supports geospatial, category, status, and text search filters via inverted indexes.
    """
    return db.get_incidents(
        category=category,
        ward=ward,
        status=status,
        min_priority=min_priority,
        search=search
    )


@router.get("/{incident_id}", response_model=Incident, summary="Get full incident intelligence dossier")
def get_incident(incident_id: str):
    """
    Fetch comprehensive incident intelligence dossier including:
    - Multimodal forensic sensor data and camera EXIF
    - AI priority explainability decomposition matrix
    - Spatio-temporal citizen report clusters
    - Field unit dispatch status and checklist
    """
    incident = db.get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' not found in active operational ledger"
        )
    return incident


@router.post("", response_model=Incident, status_code=status.HTTP_201_CREATED, summary="Ingest new citizen report")
def create_incident(report: IncidentCreate):
    """
    Ingest a new citizen or sensor incident report.
    Automatically triggers the AI deduplication engine and priority weighting model.
    """
    return db.create_incident(report.model_dump())


@router.patch("/{incident_id}/checklist/{checklist_id}", response_model=Incident, summary="Toggle mitigation procedure checklist")
def toggle_checklist(incident_id: str, checklist_id: str, completed: bool = Query(...)):
    """
    Update mitigation procedure checklist state for field dispatch tracking.
    """
    incident = db.get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' not found in active operational ledger"
        )
    if not incident.assigned_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No field unit assigned to incident '{incident_id}'"
        )

    found = False
    for item in incident.assigned_unit.checklist:
        if item.id == checklist_id:
            item.completed = completed
            found = True
            break

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checklist item '{checklist_id}' not found"
        )

    return incident
