"""
Test Suite: Dual Forensic Resolution Verification API & Officer Sign-off.
"""

from starlette.testclient import TestClient


def test_list_pending_verifications(client: TestClient):
    response = client.get("/api/v1/verification/pending")
    assert response.status_code == 200
    pending = response.json()
    assert isinstance(pending, list)
    assert len(pending) >= 1
    assert all(item["status"] == "Awaiting Verification" for item in pending)
    assert any(item["id"] == "CP-8461" for item in pending)


def test_get_forensic_evidence_valid(client: TestClient):
    response = client.get("/api/v1/verification/CP-8461")
    assert response.status_code == 200
    evidence = response.json()
    assert "before_photo_url" in evidence
    assert "after_photo_url" in evidence
    assert evidence["ai_geometric_match_score_pct"] > 80.0
    assert evidence["planar_elevation_score_pct"] > 90.0
    assert "merkle_sha256" in evidence


def test_get_forensic_evidence_missing_evidence(client: TestClient):
    # CP-8492 is active and has no forensic evidence yet
    response = client.get("/api/v1/verification/CP-8492")
    assert response.status_code == 400
    assert "does not have forensic evidence" in response.json()["error"].lower()


def test_get_forensic_evidence_not_found(client: TestClient):
    response = client.get("/api/v1/verification/CP-0000")
    assert response.status_code == 404


def test_officer_decision_approve(client: TestClient):
    payload = {
        "incident_id": "CP-8461",
        "officer_id": "OP-009",
        "officer_name": "Dir. E. Vance",
        "decision": "APPROVE",
        "notes": "LiDAR elevation meets municipal grade tolerance standard."
    }
    response = client.post("/api/v1/verification/decision", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["new_status"] == "Verified Resolved"
    assert "approved" in res["message"].lower()
    assert res["tx_block"].startswith("#TX-DECISION-")
    assert len(res["audit_hash"]) > 0


def test_officer_decision_request_proof(client: TestClient):
    payload = {
        "incident_id": "CP-8461",
        "officer_id": "OP-009",
        "officer_name": "Dir. E. Vance",
        "decision": "REQUEST_PROOF",
        "notes": "Please upload transverse camera angle."
    }
    response = client.post("/api/v1/verification/decision", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "proof requested" in res["message"].lower()


def test_officer_decision_schedule_audit(client: TestClient):
    payload = {
        "incident_id": "CP-8461",
        "officer_id": "OP-009",
        "officer_name": "Dir. E. Vance",
        "decision": "SCHEDULE_14D_AUDIT",
        "notes": "Queue mobile LiDAR route for 14-day check."
    }
    response = client.post("/api/v1/verification/decision", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "14-day" in res["message"].lower()


def test_officer_decision_reject(client: TestClient):
    payload = {
        "incident_id": "CP-8461",
        "officer_id": "OP-009",
        "officer_name": "Dir. E. Vance",
        "decision": "REJECT",
        "notes": "Asphalt compaction edge seam not sealed."
    }
    response = client.post("/api/v1/verification/decision", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["new_status"] == "In Mitigation"
    assert "rejected" in res["message"].lower()


def test_officer_decision_invalid_incident(client: TestClient):
    payload = {
        "incident_id": "CP-UNKNOWN",
        "officer_id": "OP-009",
        "officer_name": "Dir. E. Vance",
        "decision": "APPROVE"
    }
    response = client.post("/api/v1/verification/decision", json=payload)
    assert response.status_code == 404
