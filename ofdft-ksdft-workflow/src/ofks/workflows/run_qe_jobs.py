from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ofks.calculators.qe_runtime import run_qe_jobs
from ofks.io import read_jsonl, write_jsonl

app = typer.Typer(help="Run prepared Quantum ESPRESSO jobs from workflow records.")
console = Console()


@app.command()
def main(
    records: Path = typer.Option(..., "--records", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    pw_command: str = typer.Option("pw.x", "--pw-command"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    output_name: str = typer.Option("pw.out", "--output-name"),
    input_name: str = typer.Option("pw.in", "--input-name"),
    skip_existing: bool = typer.Option(True, "--skip-existing/--rerun-existing"),
    timeout_seconds: int | None = typer.Option(None, "--timeout-seconds", min=1),
    pseudo_source: Path | None = typer.Option(None, "--pseudo-source", file_okay=False, dir_okay=True),
    job_pseudo_dir: str = typer.Option("pseudo", "--job-pseudo-dir"),
) -> None:
    job_records = read_jsonl(records)
    results = run_qe_jobs(
        job_records,
        pw_command=pw_command,
        output_name=output_name,
        input_name=input_name,
        limit=limit,
        skip_existing=skip_existing,
        timeout_seconds=timeout_seconds,
        pseudo_source=pseudo_source,
        job_pseudo_dir=job_pseudo_dir,
    )
    count = write_jsonl(out, results)
    status_counts = {}
    for result in results:
        status = str(result.get("qe_run_status"))
        status_counts[status] = status_counts.get(status, 0) + 1
    console.print(f"Wrote {count} QE run records to {out}")
    console.print(f"QE run statuses: {status_counts}")


if __name__ == "__main__":
    app()
