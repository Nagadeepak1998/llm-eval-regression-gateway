from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_evaluate_endpoint_returns_report() -> None:
    response = client.post("/evaluate", json={"model_name": "candidate"})
    payload = response.json()
    assert response.status_code == 200
    assert payload["decision"] == "fail"
    assert "terraform-public-bucket" in payload["failed_cases"]


def test_metrics_endpoint_exposes_counters() -> None:
    client.post("/evaluate", json={"model_name": "baseline"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "eval_requests_total" in response.text

