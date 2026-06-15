from __future__ import annotations

from time import perf_counter

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.config import settings
from app.logging_config import configure_logging
from app.metrics import (
    evaluation_latency_seconds,
    evaluation_regressions_total,
    evaluation_requests_total,
)
from app.schemas import EvaluateRequest, EvaluateResponse
from app.service import evaluate_regression

configure_logging(settings.log_level)

app = FastAPI(title="LLM Eval Regression Gateway", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest) -> EvaluateResponse:
    started = perf_counter()
    report = evaluate_regression(request.baseline, request.candidate)
    elapsed = perf_counter() - started
    evaluation_requests_total.labels(request.baseline, request.candidate).inc()
    evaluation_latency_seconds.labels(request.baseline, request.candidate).observe(elapsed)
    evaluation_regressions_total.inc(len(report.regressions))
    return EvaluateResponse(report=report)

