import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app, follow_redirects=False)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the shared in-memory activities dict between tests."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
