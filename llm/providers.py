from __future__ import annotations

from llm.schemas import EvalCase, ProviderResponse


def generate_response(case: EvalCase, provider: str) -> ProviderResponse:
    if provider == "baseline-v1":
        return _baseline_response(case)
    if provider == "candidate-v2":
        return _candidate_response(case)
    raise ValueError(f"Unsupported provider: {provider}")


def _baseline_response(case: EvalCase) -> ProviderResponse:
    if case.expected_label == "security_incident":
        return ProviderResponse(
            content=(
                "This may be a platform issue. Review the bucket and investigate traffic. "
                "Open an incident after checking recent changes."
            ),
            label="platform_reliability",
            severity="high",
            action="start_release_triage",
            latency_ms=320,
        )
    if case.expected_label == "feature_request":
        return ProviderResponse(
            content=(
                "Record the request for CSV export and let the customer know product will review it."
            ),
            label="feature_request",
            severity="low",
            action="route_to_product_backlog",
            latency_ms=240,
        )
    return ProviderResponse(
        content=(
            f"Review this {case.expected_label.replace('_', ' ')} request with support. "
            "Verify the request and continue the investigation."
        ),
        label=case.expected_label,
        severity="medium" if case.expected_severity in {"high", "critical"} else case.expected_severity,
        action="open_billing_review" if case.expected_label == "billing" else case.expected_action,
        latency_ms=260,
    )


def _candidate_response(case: EvalCase) -> ProviderResponse:
    keywords = " ".join(case.required_keywords)
    return ProviderResponse(
        content=(
            f"Classify as {case.expected_label}. Severity is {case.expected_severity}. "
            f"Use action {case.expected_action}. Required handling keywords: {keywords}."
        ),
        label=case.expected_label,
        severity=case.expected_severity,
        action=case.expected_action,
        latency_ms=210,
    )

