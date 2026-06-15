from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_evaluate_endpoint_returns_report():
    response = client.post("/evaluate", json={"baseline": "baseline-v1", "candidate": "candidate-v2"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["report"]["baseline"]["provider"] == "baseline-v1"
    assert payload["report"]["candidate"]["provider"] == "candidate-v2"
    assert payload["report"]["regressions"] == []

