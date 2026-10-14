"""
Test Suite: Civic Transparency, Open Data (GeoJSON RFC 7946 & CSV) API.
"""

from starlette.testclient import TestClient


def test_public_trust_metrics(client: TestClient):
    response = client.get("/api/v1/transparency/metrics")
    assert response.status_code == 200
    metrics = response.json()
    assert metrics["verified_resolved_30d"] > 1000
    assert metrics["median_resolution_hours"] > 0
    assert metrics["citizen_response_sla_percent"] > 90.0
    assert metrics["taxpayer_savings_usd"] > 100000.0
    assert "Public Works & Paving" in metrics["department_benchmarks"]


def test_public_resolution_feed(client: TestClient):
    response = client.get("/api/v1/transparency/feed")
    assert response.status_code == 200
    feed = response.json()
    assert isinstance(feed, list)
    assert len(feed) >= 1


def test_export_geojson_rfc7946(client: TestClient):
    response = client.get("/api/v1/transparency/export/geojson")
    assert response.status_code == 200
    geojson = response.json()
    assert geojson["type"] == "FeatureCollection"
    assert "features" in geojson
    assert len(geojson["features"]) >= 5

    # Check first feature schema
    feature = geojson["features"][0]
    assert feature["type"] == "Feature"
    assert feature["geometry"]["type"] == "Point"
    assert len(feature["geometry"]["coordinates"]) == 2
    assert "id" in feature["properties"]
    assert "title" in feature["properties"]
    assert "priority_score" in feature["properties"]


def test_export_geojson_etag_caching(client: TestClient):
    # First request
    res1 = client.get("/api/v1/transparency/export/geojson")
    assert res1.status_code == 200
    etag = res1.headers.get("ETag")
    assert etag is not None

    # Second request with matching If-None-Match header -> 304 Not Modified
    res2 = client.get("/api/v1/transparency/export/geojson", headers={"If-None-Match": etag})
    assert res2.status_code == 304


def test_export_csv(client: TestClient):
    response = client.get("/api/v1/transparency/export/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=civicpulse_incidents.csv" in response.headers["content-disposition"]
    csv_text = response.text
    lines = csv_text.strip().split("\r\n") if "\r\n" in csv_text else csv_text.strip().split("\n")
    assert len(lines) >= 6  # Header + at least 5 incidents
    header = lines[0]
    assert "Incident ID" in header
    assert "Priority Score" in header
    assert "Audit TX Block" in header


def test_export_csv_etag_caching(client: TestClient):
    res1 = client.get("/api/v1/transparency/export/csv")
    assert res1.status_code == 200
    etag = res1.headers.get("ETag")
    assert etag is not None

    res2 = client.get("/api/v1/transparency/export/csv", headers={"If-None-Match": etag})
    assert res2.status_code == 304
