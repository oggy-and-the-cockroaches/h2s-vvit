"""
Test Suite: Incident Management & Autonomous AI Triage API.
"""

from starlette.testclient import TestClient


def test_list_incidents_default(client: TestClient):
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    # Verify default priority descending order
    scores = [item["priority_score"] for item in data]
    assert scores == sorted(scores, reverse=True)


def test_list_incidents_filter_category(client: TestClient):
    response = client.get("/api/v1/incidents?category=Electrical")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all("electrical" in inc["category"].lower() for inc in data)


def test_list_incidents_filter_ward(client: TestClient):
    response = client.get("/api/v1/incidents?ward=Ward 4")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert all("ward 4" in inc["location"]["ward"].lower() for inc in data)


def test_list_incidents_filter_status(client: TestClient):
    response = client.get("/api/v1/incidents?status=Dispatched")
    assert response.status_code == 200
    data = response.json()
    assert all(inc["status"] == "Dispatched" for inc in data)


def test_list_incidents_filter_min_priority(client: TestClient):
    response = client.get("/api/v1/incidents?min_priority=80")
    assert response.status_code == 200
    data = response.json()
    assert all(inc["priority_score"] >= 80 for inc in data)


def test_list_incidents_search_query(client: TestClient):
    response = client.get("/api/v1/incidents?search=Belmont")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "CP-8492" in [inc["id"] for inc in data]


def test_get_incident_valid(client: TestClient):
    response = client.get("/api/v1/incidents/CP-8492")
    assert response.status_code == 200
    incident = response.json()
    assert incident["id"] == "CP-8492"
    assert incident["priority_tier"] == "TIER_1_CRITICAL"
    assert incident["ai_breakdown"]["composite_priority"] == 94
    assert len(incident["citizen_reports"]) >= 4


def test_get_incident_not_found(client: TestClient):
    response = client.get("/api/v1/incidents/CP-999999")
    assert response.status_code == 404
    assert "not found" in response.json()["error"].lower()


def test_create_incident_valid(client: TestClient):
    payload = {
        "title": "Severe Gas Odor and Exposed Valve",
        "category": "Hazardous Utilities",
        "latitude": 42.3615,
        "longitude": -71.0592,
        "address": "400 Atlantic Ave",
        "ward": "Ward 3",
        "comment": "Strong rotten egg gas odor near sidewalk valve box.",
        "user_hash": "CIT-TEST-USER"
    }
    response = client.post("/api/v1/incidents", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["id"].startswith("CP-")
    assert created["title"] == payload["title"]
    assert created["status"] == "New (Unassigned)"
    assert created["ai_breakdown"] is not None
    assert created["ai_breakdown"]["composite_priority"] > 0


def test_create_incident_validation_error(client: TestClient):
    invalid_payload = {
        "title": "A",  # too short (min_length=3)
        "latitude": 200.0,  # invalid latitude (le=90.0)
    }
    response = client.post("/api/v1/incidents", json=invalid_payload)
    assert response.status_code == 422
    assert response.json()["error"] == "Validation Error"


def test_toggle_checklist_valid(client: TestClient):
    # CP-8492 has unit U-04 with checklist item chk_3 (initially False)
    response = client.patch("/api/v1/incidents/CP-8492/checklist/chk_3?completed=true")
    assert response.status_code == 200
    incident = response.json()
    checklist = incident["assigned_unit"]["checklist"]
    chk_3 = next(item for item in checklist if item["id"] == "chk_3")
    assert chk_3["completed"] is True


def test_toggle_checklist_not_found(client: TestClient):
    response = client.patch("/api/v1/incidents/CP-8492/checklist/chk_nonexistent?completed=true")
    assert response.status_code == 404
