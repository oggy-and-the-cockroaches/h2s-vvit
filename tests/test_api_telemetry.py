"""
Test Suite: Live Telemetry, Node Consensus & Health Probes.
"""

from starlette.testclient import TestClient


def test_telemetry_status(client: TestClient):
    response = client.get("/api/v1/telemetry/status")
    assert response.status_code == 200
    status_data = response.json()
    assert status_data["system_active"] is True
    assert status_data["active_incidents_count"] > 0
    assert status_data["critical_hazards_count"] > 0
    assert status_data["sync_latency_ms"] > 0


def test_validator_nodes(client: TestClient):
    response = client.get("/api/v1/telemetry/nodes")
    assert response.status_code == 200
    nodes = response.json()
    assert isinstance(nodes, list)
    assert len(nodes) == 5
    assert all(n["status"] == "ONLINE" for n in nodes)


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "healthy"
    assert "checks" in health
    assert health["checks"]["database"] == "operational"


def test_api_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    root = response.json()
    assert root["status"] == "online"
    assert "security" in root
    assert "efficiency" in root
    assert "endpoints" in root
