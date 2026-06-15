from __future__ import annotations

import argparse
import json
from pathlib import Path

from .eval_loader import load_eval_cases
from .evaluator import run_eval_suite
from .reporting import write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic LLM regression gates.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate_parser = subparsers.add_parser("evaluate", help="Run the bundled eval suite.")
    evaluate_parser.add_argument("--model", choices=["baseline", "candidate"], default="candidate")
    evaluate_parser.add_argument("--output", type=Path, default=Path("reports/latest.json"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "evaluate":
        report = run_eval_suite(load_eval_cases(), args.model)
        path = write_report(report, args.output)
        print(json.dumps({"output": str(path), "summary": report["summary"]}, indent=2))
        return 0 if report["summary"]["decision"] == "pass" else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

