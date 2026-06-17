from llm_eval_regression_gateway.eval_loader import load_eval_cases
from llm_eval_regression_gateway.evaluator import compare_eval_suites, run_eval_suite


def test_baseline_passes_eval_suite() -> None:
    report = run_eval_suite(load_eval_cases(), "baseline")
    assert report["summary"]["decision"] == "pass"
    assert report["summary"]["failed_cases"] == []


def test_candidate_fails_policy_case() -> None:
    report = run_eval_suite(load_eval_cases(), "candidate")
    assert report["summary"]["decision"] == "fail"
    assert "terraform-public-bucket" in report["summary"]["failed_cases"]


def test_compare_reports_new_failures_and_deltas() -> None:
    report = compare_eval_suites(load_eval_cases())
    comparison = report["comparison"]
    assert comparison["decision"] == "fail"
    assert comparison["new_failures"] == ["terraform-public-bucket"]
    assert comparison["recovered_cases"] == []
    assert comparison["pass_rate_delta"] == -0.25
    assert comparison["avg_score_delta"] == -0.25
