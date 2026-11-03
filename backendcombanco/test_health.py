from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_version():
    client = TestClient(app)
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == settings.app_version
    assert response.json()["status"] == "online"

