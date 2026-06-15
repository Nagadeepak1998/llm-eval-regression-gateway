from __future__ import annotations

import json
from pathlib import Path

from llm.dataset import load_eval_cases
from llm.evaluator import compare_providers


REPORT_PATH = Path(__file__).resolve().parent.parent / "reports" / "eval_report.json"


def main() -> None:
    report = compare_providers(
        cases=load_eval_cases(),
        baseline="baseline-v1",
        candidate="candidate-v2",
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report.model_dump(), indent=2) + "\n")
    print(f"Wrote regression report to {REPORT_PATH}")
    print(f"Baseline pass rate: {report.baseline.pass_rate:.2f}")
    print(f"Candidate pass rate: {report.candidate.pass_rate:.2f}")
    if report.regressions:
        print("Regressions detected:")
        for regression in report.regressions:
            print(f"- {regression}")
    else:
        print("No regressions detected.")


if __name__ == "__main__":
    main()

