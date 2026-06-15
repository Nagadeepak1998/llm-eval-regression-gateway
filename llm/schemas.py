from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Label = Literal[
    "account_access",
    "billing",
    "security_incident",
    "platform_reliability",
    "feature_request",
]
Severity = Literal["low", "medium", "high", "critical"]


class EvalCase(BaseModel):
    id: str
    prompt: str
    expected_label: Label
    expected_severity: Severity
    required_keywords: list[str]
    forbidden_keywords: list[str]
    expected_action: str


class ProviderResponse(BaseModel):
    content: str
    label: Label
    severity: Severity
    action: str
    latency_ms: int = Field(ge=1)


class CaseScore(BaseModel):
    case_id: str
    provider: str
    label_match: bool
    severity_match: bool
    action_match: bool
    required_keyword_recall: float = Field(ge=0.0, le=1.0)
    forbidden_keyword_hits: int = Field(ge=0)
    latency_ms: int = Field(ge=1)
    passed: bool


class ProviderSummary(BaseModel):
    provider: str
    pass_rate: float = Field(ge=0.0, le=1.0)
    avg_keyword_recall: float = Field(ge=0.0, le=1.0)
    label_accuracy: float = Field(ge=0.0, le=1.0)
    severity_accuracy: float = Field(ge=0.0, le=1.0)
    action_accuracy: float = Field(ge=0.0, le=1.0)
    avg_latency_ms: float = Field(ge=0.0)
    forbidden_keyword_rate: float = Field(ge=0.0, le=1.0)


class RegressionReport(BaseModel):
    baseline: ProviderSummary
    candidate: ProviderSummary
    regressions: list[str]
    case_scores: list[CaseScore]

