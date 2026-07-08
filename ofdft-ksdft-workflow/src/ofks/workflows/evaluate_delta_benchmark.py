from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.benchmarks import build_benchmark_report, render_benchmark_markdown, write_summary_csv
from ofks.io import read_jsonl, write_jsonl
from ofks.models.delta import train_delta_model
from ofks.workflows.train_delta import add_predictions, render_report

app = typer.Typer(help="Train/test evaluate a delta-corrected fast method against KSDFT labels.")
console = Console()


@app.command()
def main(
    dataset: Path = typer.Option(..., "--dataset", exists=True, file_okay=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False, dir_okay=True),
    train_fraction: float = typer.Option(0.6, "--train-fraction", min=0.1, max=0.9),
    ridge_alpha: float = typer.Option(1.0, "--ridge-alpha", min=0.0),
    truth_name: str = typer.Option("ksdft", "--truth-name"),
    raw_name: str = typer.Option("raw_fast", "--raw-name"),
    delta_name: str = typer.Option("delta_corrected", "--delta-name"),
    truth_energy_key: str = typer.Option("ks_total_energy_ev", "--truth-energy-key"),
    candidate_energy_key: str = typer.Option("total_energy_ev", "--candidate-energy-key"),
    corrected_energy_key: str = typer.Option("corrected_total_energy_ev", "--corrected-energy-key"),
    delta_key: str = typer.Option("delta_energy_pred_ev", "--delta-key"),
) -> None:
    records = read_jsonl(dataset)
    train_records, test_records = split_train_test(
        records,
        train_fraction=train_fraction,
        truth_energy_key=truth_energy_key,
        candidate_energy_key=candidate_energy_key,
    )
    if not train_records:
        raise typer.BadParameter("No trainable parsed_converged records were found for training")
    if not test_records:
        raise typer.BadParameter("No parsed_converged records were left for testing")

    out_dir.mkdir(parents=True, exist_ok=True)
    model, train_metrics = train_delta_model(
        train_records,
        ridge_alpha=ridge_alpha,
        truth_energy_key=truth_energy_key,
        candidate_energy_key=candidate_energy_key,
        corrected_energy_key=corrected_energy_key,
        delta_key=delta_key,
    )
    model_path = out_dir / "delta_model.json"
    train_report_path = out_dir / "delta_train_report.md"
    train_path = out_dir / "train_records.jsonl"
    test_path = out_dir / "test_truth.jsonl"
    raw_fast_path = out_dir / "test_raw_fast.jsonl"
    delta_pred_path = out_dir / "test_delta_corrected.jsonl"
    benchmark_json = out_dir / "benchmark.json"
    benchmark_md = out_dir / "benchmark.md"
    benchmark_csv = out_dir / "benchmark.csv"

    model.save(model_path)
    train_report_path.write_text(render_report(train_metrics, model_path), encoding="utf-8")
    write_jsonl(train_path, train_records)
    write_jsonl(test_path, test_records)
    write_jsonl(raw_fast_path, [_candidate_view(record, energy_key=candidate_energy_key) for record in test_records])
    delta_predictions = add_predictions(test_records, model)
    write_jsonl(delta_pred_path, [_candidate_view(record, energy_key=corrected_energy_key) for record in delta_predictions])

    report = build_benchmark_report(
        test_records,
        {
            raw_name: read_jsonl(raw_fast_path),
            delta_name: read_jsonl(delta_pred_path),
        },
        truth_name=truth_name,
    )
    benchmark_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    benchmark_md.write_text(render_benchmark_markdown(report), encoding="utf-8")
    write_summary_csv(report, benchmark_csv)

    console.print(f"Train records: {len(train_records)}")
    console.print(f"Test records: {len(test_records)}")
    console.print(f"Wrote delta benchmark outputs to {out_dir}")


def split_train_test(
    records: list[dict[str, Any]],
    train_fraction: float = 0.6,
    truth_energy_key: str = "ks_total_energy_ev",
    candidate_energy_key: str = "total_energy_ev",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    usable = [
        record
        for record in records
        if record.get("ks_status") == "parsed_converged"
        and record.get("converged") is not False
        and record.get("candidate_converged") is not False
        and record.get(truth_energy_key) is not None
        and record.get(candidate_energy_key) is not None
    ]
    ranked = sorted(usable, key=lambda record: str(record.get("structure_id", "")))
    if len(ranked) < 2:
        return ranked, []
    train_count = int(round(len(ranked) * train_fraction))
    train_count = max(1, min(train_count, len(ranked) - 1))
    return ranked[:train_count], ranked[train_count:]


def _candidate_view(record: dict[str, Any], energy_key: str) -> dict[str, Any]:
    candidate = {
        "structure_id": record.get("structure_id"),
        "backend": record.get("backend"),
        "candidate_name": record.get("candidate_name"),
        "converged": record.get("candidate_converged", record.get("converged")),
        "system_name": record.get("system_name"),
        "site": record.get("site"),
        "orientation": record.get("orientation"),
        "height_angstrom": record.get("height_angstrom"),
        "runtime_seconds": record.get("runtime_seconds"),
        "max_force_ev_per_ang": record.get("max_force_ev_per_ang"),
    }
    if record.get(energy_key) is not None:
        candidate[energy_key] = record.get(energy_key)
    for key in ("adsorption_energy_ev", "corrected_adsorption_energy_ev"):
        if key != energy_key and record.get(key) is not None:
            candidate[key] = record.get(key)
    if record.get("forces_ev_per_ang") is not None:
        candidate["forces_ev_per_ang"] = record.get("forces_ev_per_ang")
    if record.get("delta_energy_pred_ev") is not None:
        candidate["delta_energy_pred_ev"] = record.get("delta_energy_pred_ev")
    return candidate


if __name__ == "__main__":
    app()
