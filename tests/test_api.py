from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LLM Log Analyzer is running"


def test_analyze():
    response = client.post("/analyze", json={"log_text": "Build failed: No module named requests"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"success", "failure", "unknown"}
    assert "summary" in data
    assert "root_cause" in data
    assert "suggestion" in data