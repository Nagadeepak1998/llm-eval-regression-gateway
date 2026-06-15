from llm_eval_regression_gateway.eval_loader import load_eval_cases
from llm_eval_regression_gateway.evaluator import run_eval_suite


def test_baseline_passes_eval_suite() -> None:
    report = run_eval_suite(load_eval_cases(), "baseline")
    assert report["summary"]["decision"] == "pass"
    assert report["summary"]["failed_cases"] == []


def test_candidate_fails_policy_case() -> None:
    report = run_eval_suite(load_eval_cases(), "candidate")
    assert report["summary"]["decision"] == "fail"
    assert "terraform-public-bucket" in report["summary"]["failed_cases"]

