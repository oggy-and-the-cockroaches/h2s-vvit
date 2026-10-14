from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class IncidentPriorityTier(str, Enum):
    TIER_1_CRITICAL = "TIER_1_CRITICAL"
    TIER_2_HIGH = "TIER_2_HIGH"
    TIER_3_MODERATE = "TIER_3_MODERATE"
    TIER_4_LOW = "TIER_4_LOW"

class IncidentStatus(str, Enum):
    NEW = "New (Unassigned)"
    DISPATCHED = "Dispatched"
    IN_MITIGATION = "In Mitigation"
    AWAITING_VERIFICATION = "Awaiting Verification"
    VERIFIED_RESOLVED = "Verified Resolved"
    CLOSED = "Closed"

class DecisionType(str, Enum):
    APPROVE = "APPROVE"
    REQUEST_PROOF = "REQUEST_PROOF"
    SCHEDULE_14D_AUDIT = "SCHEDULE_14D_AUDIT"
    REJECT = "REJECT"

class GeoLocation(BaseModel):
    latitude: float
    longitude: float
    address: str
    ward: str
    sector: str = "Sector North"
    geohash: Optional[str] = None

class CitizenReport(BaseModel):
    report_id: str
    timestamp: str
    comment: str
    photo_url: Optional[str] = None
    reporter_hash: str
    distance_delta_m: Optional[float] = None
    attributes: Optional[Dict[str, Any]] = None

class ChecklistItem(BaseModel):
    id: str
    label: str
    completed: bool
    completed_at: Optional[str] = None
    completed_by: Optional[str] = None

class DispatchUnit(BaseModel):
    unit_id: str
    department: str
    squad_name: str
    lead_name: str
    crew_size: int = 2
    eta_minutes: int
    gps_ping: str
    status: str
    checklist: List[ChecklistItem] = []

class AIScoreBreakdown(BaseModel):
    composite_priority: int
    safety_urgency_pts: int = Field(..., description="Max 40 pts")
    community_impact_pts: int = Field(..., description="Max 25 pts")
    waiting_duration_pts: int = Field(..., description="Max 15 pts")
    corroboration_pts: int = Field(..., description="Max 20 pts")
    vision_confidence_pct: float
    vector_match_similarity_pct: float
    primary_hazard: str
    decision_rationale: str
    uncertainty_advisory: Optional[str] = None

class ForensicEvidence(BaseModel):
    before_photo_url: str
    after_photo_url: Optional[str] = None
    before_timestamp: str
    after_timestamp: Optional[str] = None
    before_exif: Dict[str, str] = {}
    after_exif: Dict[str, str] = {}
    ai_geometric_match_score_pct: float
    spatial_variance_m: float
    planar_elevation_score_pct: float
    spatial_landmark_match_pct: float
    edge_compaction_pct: float
    depth_metric_mm: float
    volume_loss_m3: float
    merkle_sha256: str

class Incident(BaseModel):
    id: str
    title: str
    category: str
    priority_tier: IncidentPriorityTier
    priority_score: int
    status: IncidentStatus
    location: GeoLocation
    opened_at: str
    elapsed_time: str
    sla_target: str
    corroboration_count: int
    assigned_unit: Optional[DispatchUnit] = None
    ai_breakdown: Optional[AIScoreBreakdown] = None
    citizen_reports: List[CitizenReport] = []
    forensic_evidence: Optional[ForensicEvidence] = None
    audit_tx_block: str

class IncidentCreate(BaseModel):
    title: str
    category: str
    latitude: float
    longitude: float
    address: str
    ward: str
    comment: str
    photo_url: Optional[str] = None
    user_hash: Optional[str] = "CIT-AUTO"

class DecisionRequest(BaseModel):
    incident_id: str
    officer_id: str = "OP-009"
    officer_name: str = "Dir. E. Vance"
    decision: DecisionType
    notes: Optional[str] = None

class DecisionResponse(BaseModel):
    success: bool
    incident_id: str
    decision: DecisionType
    new_status: str
    tx_block: str
    audit_hash: str
    message: str
    citizen_notifications_queued: int

class PublicTrustMetrics(BaseModel):
    verified_resolved_30d: int
    median_resolution_hours: float
    citizen_response_sla_percent: float
    taxpayer_savings_usd: float
    dual_verification_compliance_percent: float
    department_benchmarks: Dict[str, float]
    overall_trust_satisfaction_percent: int

class TelemetryStatus(BaseModel):
    system_active: bool = True
    ai_pipeline_status: str = "ACTIVE (99.8%)"
    dual_verified_standard: str = "ENFORCED"
    district: str
    node_cluster: str
    sync_latency_ms: float
    active_incidents_count: int
    critical_hazards_count: int
    awaiting_verification_count: int
    median_sla_hours: float
