"""
CivicPulse AI Operations Platform - Pytest Configuration & Test Fixtures.
"""

import sys
from pathlib import Path
import pytest
from starlette.testclient import TestClient

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from backend.app.main import app
from backend.app.data.database import db


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Session-wide TestClient configured with base URL.
    """
    with TestClient(app, base_url="http://testserver") as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_db_state():
    """
    Isolate test database state before and after each test case.
    """
    # Re-seed fresh state before each test
    db.incidents.clear()
    db._category_index.clear()
    db._ward_index.clear()
    db._status_index.clear()
    db._token_index.clear()
    db._seed_data()
    yield
