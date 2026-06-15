from __future__ import annotations

from pydantic import BaseModel

from llm.schemas import RegressionReport


class EvaluateRequest(BaseModel):
    baseline: str = "baseline-v1"
    candidate: str = "candidate-v2"


class EvaluateResponse(BaseModel):
    report: RegressionReport

