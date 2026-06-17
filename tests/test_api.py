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


def test_compare_endpoint_returns_regression_budget_result() -> None:
    response = client.post("/compare", json={"candidate_model": "candidate"})
    payload = response.json()
    assert response.status_code == 200
    assert payload["decision"] == "fail"
    assert payload["new_failures"] == ["terraform-public-bucket"]
    assert payload["baseline_model"] == "baseline"


def test_metrics_endpoint_exposes_counters() -> None:
    client.post("/evaluate", json={"model_name": "baseline"})
    client.post("/compare", json={"candidate_model": "candidate"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "eval_requests_total" in response.text
    assert "compare_requests_total" in response.text
