import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "redis" in data


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "visits" in data
    assert data["status"] == "ok"


def test_create_user():
    response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code in [200, 503]


def test_get_users():
    response = client.get("/users")
    assert response.status_code in [200, 503]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
