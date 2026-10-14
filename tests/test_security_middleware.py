"""
Test Suite: Enterprise Security Headers, Rate Limiting & Input Sanitization.
"""

from starlette.testclient import TestClient
from backend.app.core.security import sanitize_input


def test_security_headers_present(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    headers = response.headers

    # Verify Security Headers
    assert "content-security-policy" in headers
    assert "frame-ancestors 'none'" in headers["content-security-policy"]
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-content-type-options") == "nosniff"
    assert "max-age=31536000" in headers.get("strict-transport-security", "")
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert "geolocation=()" in headers.get("permissions-policy", "")
    assert headers.get("x-xss-protection") == "1; mode=block"


def test_rate_limiter_headers(client: TestClient):
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    assert "x-ratelimit-limit" in response.headers
    assert "x-ratelimit-remaining" in response.headers


def test_xss_input_sanitization_helper():
    malicious = '<script>alert("XSS")</script>Hello World <img src=x onerror=alert(1)>'
    sanitized = sanitize_input(malicious)
    assert "<script>" not in sanitized
    assert "onerror=" not in sanitized
    assert "Hello World" in sanitized


def test_xss_protection_in_incident_creation(client: TestClient):
    xss_payload = {
        "title": 'Exposed Wire <script>alert("PWNED")</script>',
        "category": "Electrical",
        "latitude": 42.36,
        "longitude": -71.06,
        "address": '100 Main St <img src=x onerror=alert("HACK")>',
        "ward": "Ward 4",
        "comment": '<script src="http://evil.com/payload.js"></script>Dangerous sparking on curb.'
    }
    response = client.post("/api/v1/incidents", json=xss_payload)
    assert response.status_code == 201
    created = response.json()
    assert "<script>" not in created["title"]
    assert "alert" not in created["title"]
    assert "onerror=" not in created["location"]["address"]
    assert "<script" not in created["citizen_reports"][0]["comment"]


def test_large_payload_rejected(client: TestClient):
    # Payload exceeding 2MB should be rejected by RequestSizeLimiterMiddleware
    huge_data = "A" * (2 * 1024 * 1024 + 100)
    response = client.post(
        "/api/v1/incidents",
        content=huge_data,
        headers={"Content-Length": str(len(huge_data)), "Content-Type": "application/json"}
    )
    assert response.status_code == 413
    assert "payload too large" in response.json()["error"].lower()
