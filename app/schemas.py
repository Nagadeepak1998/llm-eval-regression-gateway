from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvalRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str = Field(default="candidate", pattern="^(baseline|candidate)$")


class CompareRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    baseline_model: str = Field(default="baseline", pattern="^(baseline|candidate)$")
    candidate_model: str = Field(default="candidate", pattern="^(baseline|candidate)$")
    max_new_failures: int = Field(default=0, ge=0)
    min_avg_score_delta: float = -0.05
    max_avg_latency_delta_ms: float = Field(default=25.0, ge=0.0)


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


class CompareResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    baseline_model: str
    candidate_model: str
    decision: str
    new_failures: list[str]
    recovered_cases: list[str]
    new_failure_count: int
    pass_rate_delta: float
    avg_score_delta: float
    avg_latency_delta_ms: float
    regression_reasons: list[str]
    report_path: str
    markdown_output: str
