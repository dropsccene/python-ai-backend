from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_not_found():
    response = client.get("/nonexistent")
    assert response.status_code == 404
