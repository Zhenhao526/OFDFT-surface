from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl

app = typer.Typer(help="Prepare shell scripts for missing Quantum ESPRESSO jobs.")
console = Console()


@app.command()
def main(
    records: Path = typer.Option(..., "--records", exists=True, file_okay=True, dir_okay=False),
    script_out: Path = typer.Option(..., "--script-out", file_okay=True, dir_okay=False),
    missing_out: Path = typer.Option(..., "--missing-out", file_okay=True, dir_okay=False),
    pw_command: str = typer.Option("pw.x", "--pw-command"),
    limit: int | None = typer.Option(None, "--limit", min=1),
) -> None:
    all_records = read_jsonl(records)
    missing = select_missing_jobs(all_records)
    if limit is not None:
        missing = missing[:limit]
    write_qe_run_scripts(missing, script_out=script_out, pw_command=pw_command)
    write_jsonl(missing_out, missing)
    console.print(f"Prepared run scripts for {len(missing)} missing QE jobs")
    console.print(f"Wrote master script to {script_out}")
    console.print(f"Wrote missing-job records to {missing_out}")


def select_missing_jobs(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_statuses = {"input_prepared", "output_missing", "parsed_unconverged", "parse_failed", "parse_inconsistent"}
    selected = []
    for record in records:
        if not record.get("ks_job_dir") or str(record.get("ks_status")) not in missing_statuses:
            continue
        if str(record.get("ks_status")) == "parse_inconsistent":
            selected.append(record)
            continue
        output_path = Path(str(record.get("ks_output") or Path(str(record["ks_job_dir"])) / "pw.out"))
        if not _qe_output_is_complete(output_path):
            selected.append(record)
    return selected


def write_qe_run_scripts(records: list[dict[str, Any]], script_out: str | Path, pw_command: str = "pw.x") -> None:
    master = Path(script_out)
    master.parent.mkdir(parents=True, exist_ok=True)
    master_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
    ]
    for record in records:
        job_dir = Path(str(record["ks_job_dir"]))
        job_dir.mkdir(parents=True, exist_ok=True)
        job_script = job_dir / "run_qe.sh"
        job_script.write_text(_job_script_text(pw_command), encoding="utf-8")
        os.chmod(job_script, 0o755)
        master_lines.append(f"(cd {job_dir.resolve().as_posix()} && ./run_qe.sh)")
    master.write_text("\n".join(master_lines) + "\n", encoding="utf-8")
    os.chmod(master, 0o755)


def _qe_output_is_complete(output_path: Path) -> bool:
    if not output_path.exists():
        return False
    try:
        return "JOB DONE." in output_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def _job_script_text(pw_command: str) -> str:
    return "\n".join(
        [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            f"{pw_command} -in pw.in > pw.out",
            "",
        ]
    )


if __name__ == "__main__":
    app()
