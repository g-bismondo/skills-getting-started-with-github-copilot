import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

BASELINE_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state() -> None:
    activities.clear()
    activities.update(copy.deepcopy(BASELINE_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(BASELINE_ACTIVITIES))
