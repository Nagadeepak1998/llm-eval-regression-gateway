from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.config import APP_NAME, PASS_RATE_THRESHOLD, REPORT_PATH
from app.metrics import metrics
from app.schemas import EvalRequest, EvalResponse
from llm_eval_regression_gateway.eval_loader import load_eval_cases
from llm_eval_regression_gateway.evaluator import run_eval_suite
from llm_eval_regression_gateway.reporting import write_report

app = FastAPI(title=APP_NAME, version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": APP_NAME}


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    return metrics.render_prometheus()


@app.post("/evaluate", response_model=EvalResponse)
def evaluate_release(request: EvalRequest) -> EvalResponse:
    report = run_eval_suite(load_eval_cases(), request.model_name)
    report["summary"]["decision"] = (
        "pass"
        if report["summary"]["pass_rate"] >= PASS_RATE_THRESHOLD
        else "fail"
    )
    output_path = write_report(report, REPORT_PATH)
    failed = report["summary"]["decision"] != "pass"
    metrics.record_eval(report["summary"]["pass_rate"], failed)
    return EvalResponse(report_path=str(output_path), model_name=request.model_name, **report["summary"])


@app.get("/reports/latest")
def latest_report() -> dict:
    if not REPORT_PATH.exists():
        return {"status": "missing", "report_path": str(REPORT_PATH)}
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))
