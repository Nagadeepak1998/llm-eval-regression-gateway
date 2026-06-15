from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    prompt: str
    required_terms: list[str]
    forbidden_terms: list[str]
    max_latency_ms: int
    notes: str


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    passed: bool
    score: float
    latency_ms: float
    missing_terms: list[str]
    forbidden_hits: list[str]
    response: str

