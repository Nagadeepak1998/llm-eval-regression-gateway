from __future__ import annotations

import json
from pathlib import Path

from llm.schemas import EvalCase


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "eval_cases.json"


def load_eval_cases() -> list[EvalCase]:
    with DATA_PATH.open() as handle:
        raw_cases = json.load(handle)
    return [EvalCase.model_validate(item) for item in raw_cases]

