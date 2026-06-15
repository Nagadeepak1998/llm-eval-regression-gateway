from __future__ import annotations

from collections import Counter

from llm.providers import generate_response
from llm.schemas import CaseScore, EvalCase, ProviderSummary, RegressionReport


def score_provider(cases: list[EvalCase], provider: str) -> list[CaseScore]:
    scores: list[CaseScore] = []
    for case in cases:
        response = generate_response(case, provider)
        lowered_content = response.content.lower()
        matched_keywords = sum(1 for keyword in case.required_keywords if keyword in lowered_content)
        forbidden_hits = sum(1 for keyword in case.forbidden_keywords if keyword in lowered_content)
        keyword_recall = matched_keywords / len(case.required_keywords)
        label_match = response.label == case.expected_label
        severity_match = response.severity == case.expected_severity
        action_match = response.action == case.expected_action
        passed = all(
            [
                label_match,
                severity_match,
                action_match,
                forbidden_hits == 0,
                keyword_recall >= 0.75,
            ]
        )
        scores.append(
            CaseScore(
                case_id=case.id,
                provider=provider,
                label_match=label_match,
                severity_match=severity_match,
                action_match=action_match,
                required_keyword_recall=keyword_recall,
                forbidden_keyword_hits=forbidden_hits,
                latency_ms=response.latency_ms,
                passed=passed,
            )
        )
    return scores


def summarize_scores(scores: list[CaseScore], provider: str) -> ProviderSummary:
    total = len(scores)
    if total == 0:
        raise ValueError("At least one score is required")
    counts = Counter(score.passed for score in scores)
    return ProviderSummary(
        provider=provider,
        pass_rate=counts[True] / total,
        avg_keyword_recall=sum(score.required_keyword_recall for score in scores) / total,
        label_accuracy=sum(score.label_match for score in scores) / total,
        severity_accuracy=sum(score.severity_match for score in scores) / total,
        action_accuracy=sum(score.action_match for score in scores) / total,
        avg_latency_ms=sum(score.latency_ms for score in scores) / total,
        forbidden_keyword_rate=sum(score.forbidden_keyword_hits > 0 for score in scores) / total,
    )


def compare_providers(cases: list[EvalCase], baseline: str, candidate: str) -> RegressionReport:
    baseline_scores = score_provider(cases, baseline)
    candidate_scores = score_provider(cases, candidate)
    baseline_summary = summarize_scores(baseline_scores, baseline)
    candidate_summary = summarize_scores(candidate_scores, candidate)

    regressions: list[str] = []
    if candidate_summary.pass_rate < baseline_summary.pass_rate:
        regressions.append("candidate pass rate is lower than baseline")
    if candidate_summary.label_accuracy < baseline_summary.label_accuracy:
        regressions.append("candidate label accuracy is lower than baseline")
    if candidate_summary.avg_keyword_recall < baseline_summary.avg_keyword_recall:
        regressions.append("candidate keyword recall is lower than baseline")
    if candidate_summary.forbidden_keyword_rate > baseline_summary.forbidden_keyword_rate:
        regressions.append("candidate forbidden keyword rate is worse than baseline")
    if candidate_summary.avg_latency_ms > baseline_summary.avg_latency_ms * 1.25:
        regressions.append("candidate latency exceeds 125 percent of baseline")

    return RegressionReport(
        baseline=baseline_summary,
        candidate=candidate_summary,
        regressions=regressions,
        case_scores=baseline_scores + candidate_scores,
    )

