from __future__ import annotations

from prometheus_client import Counter, Histogram


evaluation_requests_total = Counter(
    "evaluation_requests_total",
    "Total evaluation requests.",
    labelnames=("baseline", "candidate"),
)
evaluation_latency_seconds = Histogram(
    "evaluation_latency_seconds",
    "Evaluation request latency in seconds.",
    labelnames=("baseline", "candidate"),
)
evaluation_regressions_total = Counter(
    "evaluation_regressions_total",
    "Total regressions found by the gateway.",
)

