import json
from pathlib import Path

from llm_eval_regression_gateway.cli import main


def test_cli_writes_report(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "report.json"
    monkeypatch.setattr(
        "sys.argv",
        ["llm-eval-gateway", "evaluate", "--model", "baseline", "--output", str(output)],
    )
    exit_code = main()
    assert exit_code == 0
    assert output.exists()


def test_cli_compare_writes_report(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "compare.json"
    markdown = tmp_path / "compare.md"
    monkeypatch.setattr(
        "sys.argv",
        [
            "llm-eval-gateway",
            "compare",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ],
    )
    exit_code = main()
    assert exit_code == 1
    assert output.exists()
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["comparison"]["new_failures"] == ["terraform-public-bucket"]
    assert markdown.exists()


def test_cli_writes_markdown_and_junit(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "report.json"
    markdown = tmp_path / "summary.md"
    junit = tmp_path / "results.xml"
    monkeypatch.setattr(
        "sys.argv",
        [
            "llm-eval-gateway",
            "evaluate",
            "--model",
            "candidate",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
            "--junit-output",
            str(junit),
        ],
    )
    exit_code = main()
    assert exit_code == 1
    assert output.exists()
    assert markdown.exists()
    assert junit.exists()
    assert "<testsuite" in junit.read_text(encoding="utf-8")
