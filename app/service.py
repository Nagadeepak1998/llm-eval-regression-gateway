from __future__ import annotations

from llm.dataset import load_eval_cases
from llm.evaluator import compare_providers
from llm.schemas import RegressionReport


def evaluate_regression(baseline: str, candidate: str) -> RegressionReport:
    return compare_providers(load_eval_cases(), baseline=baseline, candidate=candidate)

