from __future__ import annotations

import json
from pathlib import Path

from .eval_types import EvalCase


def default_evalset_path() -> Path:
    return Path(__file__).resolve().parents[2] / "evals" / "support_evalset.jsonl"


def load_eval_cases(path: Path | None = None) -> list[EvalCase]:
    eval_path = path or default_evalset_path()
    cases: list[EvalCase] = []
    with eval_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            item = json.loads(line)
            cases.append(
                EvalCase(
                    case_id=item["case_id"],
                    prompt=item["prompt"],
                    required_terms=item["required_terms"],
                    forbidden_terms=item["forbidden_terms"],
                    max_latency_ms=item["max_latency_ms"],
                    notes=item["notes"],
                )
            )
    return cases

