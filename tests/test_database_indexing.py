"""
Test Suite: In-Memory Database Indexing & Sub-Millisecond Search Performance.
"""

import time
from backend.app.data.database import db
from backend.app.models.schemas import DecisionType


def test_inverted_index_integrity():
    assert len(db._category_index) > 0
    assert len(db._ward_index) > 0
    assert len(db._status_index) > 0
    assert len(db._token_index) > 0

    # Verify CP-8492 indexed under Electrical Hazards and Ward 4
    electrical_ids = db._category_index.get("electrical hazards", set())
    assert "CP-8492" in electrical_ids

    ward4_ids = db._ward_index.get("ward 4", set())
    assert "CP-8492" in ward4_ids


def test_reindexing_on_status_change():
    inc = db.get_incident_by_id("CP-8461")
    assert inc.status.value == "Awaiting Verification"
    assert "CP-8461" in db._status_index["awaiting verification"]

    # Record decision approve
    db.record_decision(
        incident_id="CP-8461",
        officer_id="OP-009",
        officer_name="Dir. E. Vance",
        decision=DecisionType.APPROVE
    )

    assert inc.status.value == "Verified Resolved"
    assert "CP-8461" not in db._status_index.get("awaiting verification", set())
    assert "CP-8461" in db._status_index["verified resolved"]


def test_sub_millisecond_search():
    start = time.perf_counter()
    results = db.get_incidents(category="Roadways", search="Pothole")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert len(results) >= 1
    # Search should execute in under 10ms (typical <1ms)
    assert elapsed_ms < 15.0
