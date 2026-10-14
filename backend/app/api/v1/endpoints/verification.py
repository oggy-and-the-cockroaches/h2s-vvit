from typing import List
from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import (
    Incident, ForensicEvidence, DecisionRequest, DecisionResponse, IncidentStatus
)
from backend.app.data.database import db

router = APIRouter(prefix="/verification", tags=["Resolution Verification"])

@router.get("/pending", response_model=List[Incident], summary="List incidents awaiting verification")
def list_pending_verifications():
    """
    Retrieve all incidents flagged as crew-complete and awaiting statutory dual officer sign-off.
    """
    return [
        inc for inc in db.incidents.values()
        if inc.status == IncidentStatus.AWAITING_VERIFICATION
    ]

@router.get("/{incident_id}", response_model=ForensicEvidence, summary="Get forensic comparison evidence for incident")
def get_forensic_evidence(incident_id: str):
    """
    Get dual before/after photogrammetry data, LiDAR elevation scores,
    and camera EXIF records for verification audit.
    """
    incident = db.get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")
    if not incident.forensic_evidence:
        raise HTTPException(status_code=400, detail=f"Incident '{incident_id}' does not have forensic evidence submitted yet")
    return incident.forensic_evidence

@router.post("/decision", response_model=DecisionResponse, summary="Submit officer sign-off decision")
def submit_officer_decision(decision_req: DecisionRequest):
    """
    Execute statutory officer sign-off action:
    - APPROVE: Signs off and unlocks contractor milestone invoice
    - REQUEST_PROOF: Dispatches request for additional photos
    - SCHEDULE_14D_AUDIT: Queues automated mobile LiDAR re-scan
    - REJECT: Reissues non-conformance notice and resets SLA
    """
    try:
        response = db.record_decision(
            incident_id=decision_req.incident_id,
            officer_id=decision_req.officer_id,
            officer_name=decision_req.officer_name,
            decision=decision_req.decision,
            notes=decision_req.notes
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
