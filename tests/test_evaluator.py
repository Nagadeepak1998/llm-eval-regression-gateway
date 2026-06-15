from llm.dataset import load_eval_cases
from llm.evaluator import compare_providers


def test_candidate_beats_baseline_on_pass_rate():
    report = compare_providers(load_eval_cases(), "baseline-v1", "candidate-v2")
    assert report.candidate.pass_rate > report.baseline.pass_rate
    assert report.regressions == []


def test_baseline_has_known_security_misclassification():
    report = compare_providers(load_eval_cases(), "baseline-v1", "candidate-v2")
    baseline_scores = [score for score in report.case_scores if score.provider == "baseline-v1"]
    security_score = next(score for score in baseline_scores if score.case_id == "security-breach-001")
    assert security_score.label_match is False
    assert security_score.passed is False

