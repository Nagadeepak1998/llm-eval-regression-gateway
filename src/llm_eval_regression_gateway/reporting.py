from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring


def with_generated_at(report: dict) -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        **report,
    }


def write_report(report: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = with_generated_at(report)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output_path


def write_eval_markdown(report: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = report["summary"]
    failed_cases = summary["failed_cases"] or ["None"]
    lines = [
        "# LLM Eval Summary",
        "",
        f"- Model: `{report['model_name']}`",
        f"- Decision: `{summary['decision']}`",
        f"- Pass rate: `{summary['pass_rate']}`",
        f"- Average score: `{summary['avg_score']}`",
        f"- Average latency ms: `{summary['avg_latency_ms']}`",
        "",
        "## Failed Cases",
        "",
        *[f"- `{case_id}`" if case_id != "None" else "- None" for case_id in failed_cases],
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def write_compare_markdown(report: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison = report["comparison"]
    new_failures = comparison["new_failures"] or ["None"]
    recovered_cases = comparison["recovered_cases"] or ["None"]
    lines = [
        "# LLM Eval Comparison",
        "",
        f"- Baseline model: `{report['baseline']['model_name']}`",
        f"- Candidate model: `{report['candidate']['model_name']}`",
        f"- Decision: `{comparison['decision']}`",
        f"- New failure count: `{comparison['new_failure_count']}`",
        f"- Pass rate delta: `{comparison['pass_rate_delta']}`",
        f"- Average score delta: `{comparison['avg_score_delta']}`",
        f"- Average latency delta ms: `{comparison['avg_latency_delta_ms']}`",
        "",
        "## Regression Budget",
        "",
        f"- Max new failures: `{comparison['regression_budget']['max_new_failures']}`",
        f"- Min average score delta: `{comparison['regression_budget']['min_avg_score_delta']}`",
        (
            "- Max average latency delta ms: "
            f"`{comparison['regression_budget']['max_avg_latency_delta_ms']}`"
        ),
        "",
        "## New Failures",
        "",
        *[f"- `{case_id}`" if case_id != "None" else "- None" for case_id in new_failures],
        "",
        "## Recovered Cases",
        "",
        *[f"- `{case_id}`" if case_id != "None" else "- None" for case_id in recovered_cases],
        "",
        "## Budget Outcome",
        "",
        *(
            [f"- {reason}" for reason in comparison["regression_reasons"]]
            if comparison["regression_reasons"]
            else ["- No budget thresholds were exceeded."]
        ),
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def write_junit_xml(report: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results = report["results"]
    suite = Element(
        "testsuite",
        name=f"llm-eval-{report['model_name']}",
        tests=str(len(results)),
        failures=str(sum(1 for result in results if not result["passed"])),
    )
    for result in results:
        case = SubElement(
            suite,
            "testcase",
            name=result["case_id"],
            classname=f"llm_eval.{report['model_name']}",
            time=f"{result['latency_ms'] / 1000:.6f}",
        )
        if not result["passed"]:
            failure = SubElement(case, "failure", message="eval regression")
            failure.text = json.dumps(
                {
                    "missing_terms": result["missing_terms"],
                    "forbidden_hits": result["forbidden_hits"],
                    "score": result["score"],
                },
                indent=2,
            )
    output_path.write_text(tostring(suite, encoding="unicode") + "\n", encoding="utf-8")
    return output_path
