from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ofks.benchmarks import build_benchmark_report, render_benchmark_markdown, write_summary_csv
from ofks.io import read_jsonl

app = typer.Typer(help="Benchmark candidate algorithms against KSDFT reference labels.")
console = Console()


@app.command()
def main(
    truth: Path = typer.Option(..., "--truth", exists=True, file_okay=True, dir_okay=False),
    candidate: Annotated[
        list[str],
        typer.Option(
            "--candidate",
            help="Candidate algorithm as name=path. Repeat for multiple algorithms.",
        ),
    ] = [],
    out_json: Path = typer.Option(..., "--out-json", file_okay=True, dir_okay=False),
    out_md: Path | None = typer.Option(None, "--out-md", file_okay=True, dir_okay=False),
    out_csv: Path | None = typer.Option(None, "--out-csv", file_okay=True, dir_okay=False),
    truth_name: str = typer.Option("ksdft", "--truth-name"),
) -> None:
    truth_records = read_jsonl(truth)
    candidates = _load_candidates(candidate)
    report = build_benchmark_report(truth_records, candidates, truth_name=truth_name)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    console.print(f"Wrote benchmark JSON to {out_json}")

    if out_md is not None:
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_benchmark_markdown(report), encoding="utf-8")
        console.print(f"Wrote benchmark report to {out_md}")

    if out_csv is not None:
        write_summary_csv(report, out_csv)
        console.print(f"Wrote benchmark CSV to {out_csv}")

    for algorithm in report["algorithms"]:
        console.print(
            f"{algorithm['name']}: matched={algorithm['n_matched']}, "
            f"aligned_MAE={algorithm.get('energy_aligned_mae_ev')}"
        )


def _load_candidates(items: list[str]) -> dict[str, list[dict[str, object]]]:
    if not items:
        raise typer.BadParameter("Provide at least one --candidate name=path")
    candidates: dict[str, list[dict[str, object]]] = {}
    for item in items:
        if "=" not in item:
            raise typer.BadParameter(f"Candidate must be name=path, got: {item}")
        name, raw_path = item.split("=", 1)
        name = name.strip()
        path = Path(raw_path.strip())
        if not name:
            raise typer.BadParameter(f"Candidate name is empty: {item}")
        if not path.exists():
            raise typer.BadParameter(f"Candidate file does not exist: {path}")
        candidates[name] = read_jsonl(path)
    return candidates


if __name__ == "__main__":
    app()
