"""
CivicPulse AI Operations Platform - Data Models & Pydantic Schemas.

Defines validated schemas for incidents, geospatial anchors, citizen reports,
dispatch checklists, multimodal forensic evidence, officer sign-off decisions,
and public transparency metrics.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from backend.app.core.security import sanitize_input


class IncidentPriorityTier(str, Enum):
    """Priority classification tier determined by AI triage engine."""
    TIER_1_CRITICAL = "TIER_1_CRITICAL"
    TIER_2_HIGH = "TIER_2_HIGH"
    TIER_3_MODERATE = "TIER_3_MODERATE"
    TIER_4_LOW = "TIER_4_LOW"


class IncidentStatus(str, Enum):
    """Operational lifecycle state of a municipal incident."""
    NEW = "New (Unassigned)"
    DISPATCHED = "Dispatched"
    IN_MITIGATION = "In Mitigation"
    AWAITING_VERIFICATION = "Awaiting Verification"
    VERIFIED_RESOLVED = "Verified Resolved"
    CLOSED = "Closed"


class DecisionType(str, Enum):
    """Statutory officer sign-off decision action."""
    APPROVE = "APPROVE"
    REQUEST_PROOF = "REQUEST_PROOF"
    SCHEDULE_14D_AUDIT = "SCHEDULE_14D_AUDIT"
    REJECT = "REJECT"


class GeoLocation(BaseModel):
    """Geospatial coordinates and administrative ward classification."""
    latitude: float = Field(..., ge=-90.0, le=90.0, description="WGS84 Latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="WGS84 Longitude")
    address: str = Field(..., min_length=3, max_length=200, description="Cross street or street address")
    ward: str = Field(..., min_length=2, max_length=50, description="Municipal ward identifier")
    sector: str = Field(default="Sector North", max_length=50)
    geohash: Optional[str] = Field(default=None, max_length=12)

    @field_validator("address", "ward", "sector", mode="before")
    @classmethod
    def sanitize_geo_strings(cls, v: Any) -> Any:
        if isinstance(v, str):
            return sanitize_input(v)
        return v


class CitizenReport(BaseModel):
    """Crowdsourced resident or sensor incident submission."""
    report_id: str = Field(..., min_length=3, max_length=50)
    timestamp: str = Field(..., max_length=50)
    comment: str = Field(..., min_length=1, max_length=1000)
    photo_url: Optional[str] = Field(default=None, max_length=1000)
    reporter_hash: str = Field(..., max_length=128)
    distance_delta_m: Optional[float] = Field(default=None, ge=0.0)
    attributes: Optional[Dict[str, Any]] = None

    @field_validator("comment", mode="before")
    @classmethod
    def sanitize_comment(cls, v: Any) -> Any:
        if isinstance(v, str):
            return sanitize_input(v)
        return v


class ChecklistItem(BaseModel):
    """Operational procedure step for field dispatch mitigation."""
    id: str = Field(..., min_length=1, max_length=50)
    label: str = Field(..., min_length=1, max_length=200)
    completed: bool = False
    completed_at: Optional[str] = Field(default=None, max_length=50)
    completed_by: Optional[str] = Field(default=None, max_length=100)


class DispatchUnit(BaseModel):
    """Municipal service squad and field vehicle telemetry."""
    unit_id: str = Field(..., min_length=1, max_length=50)
    department: str = Field(..., min_length=2, max_length=150)
    squad_name: str = Field(..., min_length=2, max_length=150)
    lead_name: str = Field(..., min_length=2, max_length=100)
    crew_size: int = Field(default=2, ge=1, le=20)
    eta_minutes: int = Field(..., ge=0, le=1440)
    gps_ping: str = Field(..., max_length=100)
    status: str = Field(..., max_length=100)
    checklist: List[ChecklistItem] = []


class AIScoreBreakdown(BaseModel):
    """Explainable AI priority composite scoring decomposition."""
    composite_priority: int = Field(..., ge=0, le=100, description="Overall urgency score (1-100)")
    safety_urgency_pts: int = Field(..., ge=0, le=40, description="Safety hazard rating (max 40 pts)")
    community_impact_pts: int = Field(..., ge=0, le=25, description="Population & infrastructure impact (max 25 pts)")
    waiting_duration_pts: int = Field(..., ge=0, le=15, description="SLA waiting penalty (max 15 pts)")
    corroboration_pts: int = Field(..., ge=0, le=20, description="Corroboration concordance (max 20 pts)")
    vision_confidence_pct: float = Field(..., ge=0.0, le=100.0)
    vector_match_similarity_pct: float = Field(..., ge=0.0, le=100.0)
    primary_hazard: str = Field(..., max_length=200)
    decision_rationale: str = Field(..., max_length=500)
    uncertainty_advisory: Optional[str] = Field(default=None, max_length=500)


class ForensicEvidence(BaseModel):
    """Photogrammetric before/after imagery, LiDAR depth metrics, and Merkle proof."""
    before_photo_url: str = Field(..., max_length=1000)
    after_photo_url: Optional[str] = Field(default=None, max_length=1000)
    before_timestamp: str = Field(..., max_length=50)
    after_timestamp: Optional[str] = Field(default=None, max_length=50)
    before_exif: Dict[str, str] = {}
    after_exif: Dict[str, str] = {}
    ai_geometric_match_score_pct: float = Field(..., ge=0.0, le=100.0)
    spatial_variance_m: float = Field(..., ge=0.0)
    planar_elevation_score_pct: float = Field(..., ge=0.0, le=100.0)
    spatial_landmark_match_pct: float = Field(..., ge=0.0, le=100.0)
    edge_compaction_pct: float = Field(..., ge=0.0, le=100.0)
    depth_metric_mm: float = Field(..., description="Elevation depth in millimeters (negative for depression)")
    volume_loss_m3: float = Field(..., ge=0.0)
    merkle_sha256: str = Field(..., max_length=128)


class Incident(BaseModel):
    """Unified incident intelligence record."""
    id: str = Field(..., min_length=2, max_length=30)
    title: str = Field(..., min_length=3, max_length=200)
    category: str = Field(..., min_length=2, max_length=100)
    priority_tier: IncidentPriorityTier
    priority_score: int = Field(..., ge=0, le=100)
    status: IncidentStatus
    location: GeoLocation
    opened_at: str = Field(..., max_length=50)
    elapsed_time: str = Field(..., max_length=50)
    sla_target: str = Field(..., max_length=50)
    corroboration_count: int = Field(default=1, ge=0)
    assigned_unit: Optional[DispatchUnit] = None
    ai_breakdown: Optional[AIScoreBreakdown] = None
    citizen_reports: List[CitizenReport] = []
    forensic_evidence: Optional[ForensicEvidence] = None
    audit_tx_block: str = Field(..., max_length=100)


class IncidentCreate(BaseModel):
    """Payload schema for ingesting a new incident report."""
    title: str = Field(..., min_length=3, max_length=200, description="Short incident summary")
    category: str = Field(..., min_length=2, max_length=100, description="Incident category")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="WGS84 Latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="WGS84 Longitude")
    address: str = Field(..., min_length=3, max_length=200, description="Incident address")
    ward: str = Field(..., min_length=2, max_length=50, description="Municipal ward")
    comment: str = Field(..., min_length=1, max_length=1000, description="Citizen details or observation")
    photo_url: Optional[str] = Field(default=None, max_length=1000)
    user_hash: Optional[str] = Field(default="CIT-AUTO", max_length=100)

    @field_validator("title", "category", "address", "ward", "comment", mode="before")
    @classmethod
    def sanitize_incoming_strings(cls, v: Any) -> Any:
        if isinstance(v, str):
            return sanitize_input(v)
        return v


class DecisionRequest(BaseModel):
    """Payload schema for an officer sign-off decision."""
    incident_id: str = Field(..., min_length=2, max_length=30)
    officer_id: str = Field(default="OP-009", min_length=2, max_length=50)
    officer_name: str = Field(default="Dir. E. Vance", min_length=2, max_length=100)
    decision: DecisionType
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("incident_id", "officer_id", "officer_name", "notes", mode="before")
    @classmethod
    def sanitize_decision_fields(cls, v: Any) -> Any:
        if isinstance(v, str):
            return sanitize_input(v)
        return v


class DecisionResponse(BaseModel):
    """Response returned upon statutory officer sign-off execution."""
    success: bool
    incident_id: str
    decision: DecisionType
    new_status: str
    tx_block: str
    audit_hash: str
    message: str
    citizen_notifications_queued: int


class PublicTrustMetrics(BaseModel):
    """Municipal civic accountability and performance metrics."""
    verified_resolved_30d: int = Field(..., ge=0)
    median_resolution_hours: float = Field(..., ge=0.0)
    citizen_response_sla_percent: float = Field(..., ge=0.0, le=100.0)
    taxpayer_savings_usd: float = Field(..., ge=0.0)
    dual_verification_compliance_percent: float = Field(..., ge=0.0, le=100.0)
    department_benchmarks: Dict[str, float]
    overall_trust_satisfaction_percent: int = Field(..., ge=0, le=100)


class TelemetryStatus(BaseModel):
    """Real-time platform heartbeat and validator consensus status."""
    system_active: bool = True
    ai_pipeline_status: str = "ACTIVE (99.8%)"
    dual_verified_standard: str = "ENFORCED"
    district: str
    node_cluster: str
    sync_latency_ms: float = Field(..., ge=0.0)
    active_incidents_count: int = Field(..., ge=0)
    critical_hazards_count: int = Field(..., ge=0)
    awaiting_verification_count: int = Field(..., ge=0)
    median_sla_hours: float = Field(..., ge=0.0)
