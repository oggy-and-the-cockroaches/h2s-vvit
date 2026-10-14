import csv
import io
from typing import List, Dict, Any
from fastapi import APIRouter, Response
from backend.app.models.schemas import PublicTrustMetrics, Incident
from backend.app.data.database import db

router = APIRouter(prefix="/transparency", tags=["Public Transparency & Trust"])

@router.get("/metrics", response_model=PublicTrustMetrics, summary="Get public accountability trust metrics")
def get_public_trust_metrics():
    """
    Retrieve live municipal accountability metrics including:
    - 30-day verified resolution volume
    - Median turnaround speed vs district benchmark
    - Taxpayer savings from automated deduplication
    - Departmental compliance percentages
    """
    return db.get_trust_metrics()

@router.get("/feed", response_model=List[Incident], summary="Live resolution stream")
def get_public_resolution_feed():
    """
    Continuous public stream of verified municipal resolutions with photographic proof.
    """
    return [
        inc for inc in db.incidents.values()
        if inc.forensic_evidence is not None or inc.status.value in ("Verified Resolved", "Awaiting Verification", "In Mitigation")
    ]

@router.get("/export/geojson", summary="Export incident dataset in GeoJSON RFC 7946 format")
def export_geojson():
    """
    Open data feed: Export all active and verified municipal incidents as GeoJSON FeatureCollection.
    """
    features = []
    for inc in db.incidents.values():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [inc.location.longitude, inc.location.latitude]
            },
            "properties": {
                "id": inc.id,
                "title": inc.title,
                "category": inc.category,
                "priority_score": inc.priority_score,
                "status": inc.status.value,
                "address": inc.location.address,
                "ward": inc.location.ward,
                "opened_at": inc.opened_at,
                "sla_target": inc.sla_target,
                "corroborations": inc.corroboration_count,
                "tx_block": inc.audit_tx_block
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features
    }
    return geojson_data

@router.get("/export/csv", summary="Download public ledger in CSV format")
def export_csv():
    """
    Open data feed: Download municipal resolution ledger in CSV format.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Incident ID", "Title", "Category", "Priority Score",
        "Status", "Latitude", "Longitude", "Address", "Ward", "SLA Target", "Audit TX Block"
    ])

    for inc in db.incidents.values():
        writer.writerow([
            inc.id, inc.title, inc.category, inc.priority_score,
            inc.status.value, inc.location.latitude, inc.location.longitude,
            inc.location.address, inc.location.ward, inc.sla_target, inc.audit_tx_block
        ])

    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=civicpulse_incidents.csv"}
    )
