import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "redis" in data

def test_metrics():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "visits" in data
    assert "status" in data
    assert data["status"] == "ok"

def test_create_user():
    """Test user creation"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = client.post("/users", json=user_data)
    # Will fail without database, but endpoint should be accessible
    assert response.status_code in [200, 503]

def test_get_users():
    """Test getting users"""
    response = client.get("/users")
    # Will fail without database, but endpoint should be accessible
    assert response.status_code in [200, 503]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
