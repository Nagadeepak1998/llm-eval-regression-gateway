from __future__ import annotations

from statistics import mean
from time import perf_counter

from .demo_models import generate_response
from .eval_types import EvalCase, EvalResult


def evaluate_case(case: EvalCase, model_name: str) -> EvalResult:
    start = perf_counter()
    response = generate_response(model_name, case.prompt)
    latency_ms = (perf_counter() - start) * 1000
    normalized_response = response.lower()
    missing_terms = [term for term in case.required_terms if term.lower() not in normalized_response]
    forbidden_hits = [term for term in case.forbidden_terms if term.lower() in normalized_response]
    latency_penalty = 0.0 if latency_ms <= case.max_latency_ms else 0.2
    term_penalty = 0.25 * len(missing_terms)
    forbidden_penalty = 0.5 * len(forbidden_hits)
    score = max(0.0, 1.0 - latency_penalty - term_penalty - forbidden_penalty)
    passed = not missing_terms and not forbidden_hits and latency_ms <= case.max_latency_ms
    return EvalResult(
        case_id=case.case_id,
        passed=passed,
        score=round(score, 3),
        latency_ms=round(latency_ms, 2),
        missing_terms=missing_terms,
        forbidden_hits=forbidden_hits,
        response=response,
    )


def summarize_results(results: list[EvalResult], pass_rate_threshold: float = 1.0) -> dict:
    if not results:
        raise ValueError("at least one result is required")
    pass_count = sum(1 for result in results if result.passed)
    pass_rate = pass_count / len(results)
    avg_score = mean(result.score for result in results)
    avg_latency_ms = mean(result.latency_ms for result in results)
    decision = "pass" if pass_rate >= pass_rate_threshold else "fail"
    return {
        "decision": decision,
        "pass_rate": round(pass_rate, 3),
        "avg_score": round(avg_score, 3),
        "avg_latency_ms": round(avg_latency_ms, 2),
        "failed_cases": [result.case_id for result in results if not result.passed],
        "total_cases": len(results),
        "passed_cases": pass_count,
    }


def run_eval_suite(cases: list[EvalCase], model_name: str) -> dict:
    results = [evaluate_case(case, model_name) for case in cases]
    summary = summarize_results(results)
    return {
        "model_name": model_name,
        "summary": summary,
        "results": [
            {
                "case_id": result.case_id,
                "passed": result.passed,
                "score": result.score,
                "latency_ms": result.latency_ms,
                "missing_terms": result.missing_terms,
                "forbidden_hits": result.forbidden_hits,
                "response": result.response,
            }
            for result in results
        ],
    }
