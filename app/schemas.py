from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvalRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str = Field(default="candidate", pattern="^(baseline|candidate)$")


class EvalResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str
    decision: str
    pass_rate: float
    avg_score: float
    avg_latency_ms: float
    failed_cases: list[str]
    total_cases: int
    passed_cases: int
    report_path: str
