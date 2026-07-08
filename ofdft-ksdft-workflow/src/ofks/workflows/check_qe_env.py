from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ofks.calculators.qe_runtime import check_qe_environment, render_qe_environment_report
from ofks.config import load_yaml

app = typer.Typer(help="Check local Quantum ESPRESSO command and pseudopotential availability.")
console = Console()


@app.command()
def main(
    calculator: Path = typer.Option(..., "--calculator", exists=True, file_okay=True, dir_okay=False),
    pw_command: str = typer.Option("pw.x", "--pw-command"),
    base_dir: Path = typer.Option(Path("."), "--base-dir", file_okay=False, dir_okay=True),
    report_out: Path | None = typer.Option(None, "--report-out", file_okay=True, dir_okay=False),
    strict: bool = typer.Option(False, "--strict"),
) -> None:
    config = load_yaml(calculator)
    check = check_qe_environment(config, pw_command=pw_command, base_dir=base_dir)
    report = render_qe_environment_report(check)
    if report_out is not None:
        report_out.parent.mkdir(parents=True, exist_ok=True)
        report_out.write_text(report, encoding="utf-8")
        console.print(f"Wrote QE environment report to {report_out}")
    else:
        console.print(report)
    if strict and not check.ok:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
