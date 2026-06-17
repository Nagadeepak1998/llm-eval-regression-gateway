from __future__ import annotations

import argparse
import json
from pathlib import Path

from .eval_loader import load_eval_cases
from .evaluator import compare_eval_suites, run_eval_suite
from .reporting import (
    write_compare_markdown,
    write_eval_markdown,
    write_junit_xml,
    write_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic LLM regression gates.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate_parser = subparsers.add_parser("evaluate", help="Run the bundled eval suite.")
    evaluate_parser.add_argument("--model", choices=["baseline", "candidate"], default="candidate")
    evaluate_parser.add_argument("--output", type=Path, default=Path("reports/latest.json"))
    evaluate_parser.add_argument("--markdown-output", type=Path)
    evaluate_parser.add_argument("--junit-output", type=Path)

    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare candidate results against a baseline regression budget.",
    )
    compare_parser.add_argument("--baseline-model", choices=["baseline", "candidate"], default="baseline")
    compare_parser.add_argument("--candidate-model", choices=["baseline", "candidate"], default="candidate")
    compare_parser.add_argument("--max-new-failures", type=int, default=0)
    compare_parser.add_argument("--min-avg-score-delta", type=float, default=-0.05)
    compare_parser.add_argument("--max-avg-latency-delta-ms", type=float, default=25.0)
    compare_parser.add_argument("--output", type=Path, default=Path("reports/compare.json"))
    compare_parser.add_argument("--markdown-output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "evaluate":
        report = run_eval_suite(load_eval_cases(), args.model)
        path = write_report(report, args.output)
        if args.markdown_output:
            write_eval_markdown(report, args.markdown_output)
        if args.junit_output:
            write_junit_xml(report, args.junit_output)
        print(json.dumps({"output": str(path), "summary": report["summary"]}, indent=2))
        return 0 if report["summary"]["decision"] == "pass" else 1
    if args.command == "compare":
        report = compare_eval_suites(
            load_eval_cases(),
            baseline_model=args.baseline_model,
            candidate_model=args.candidate_model,
            max_new_failures=args.max_new_failures,
            min_avg_score_delta=args.min_avg_score_delta,
            max_avg_latency_delta_ms=args.max_avg_latency_delta_ms,
        )
        path = write_report(report, args.output)
        if args.markdown_output:
            write_compare_markdown(report, args.markdown_output)
        print(json.dumps({"output": str(path), "comparison": report["comparison"]}, indent=2))
        return 0 if report["comparison"]["decision"] == "pass" else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
