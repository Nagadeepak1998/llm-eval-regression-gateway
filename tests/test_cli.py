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

