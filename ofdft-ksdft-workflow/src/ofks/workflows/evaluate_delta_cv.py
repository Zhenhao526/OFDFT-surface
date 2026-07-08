from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.benchmarks import build_benchmark_report, render_benchmark_markdown, write_summary_csv
from ofks.io import read_jsonl, write_jsonl
from ofks.models.delta import train_delta_model
from ofks.workflows.train_delta import add_predictions

app = typer.Typer(help="Run deterministic K-fold delta-learning evaluation against KSDFT labels.")
console = Console()


@app.command()
def main(
    dataset: Path = typer.Option(..., "--dataset", exists=True, file_okay=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False, dir_okay=True),
    folds: int = typer.Option(4, "--folds", min=2),
    ridge_alpha: float = typer.Option(1.0, "--ridge-alpha", min=0.0),
    truth_name: str = typer.Option("ksdft", "--truth-name"),
    raw_name: str = typer.Option("raw_fast_cv", "--raw-name"),
    delta_name: str = typer.Option("delta_cv", "--delta-name"),
    truth_energy_key: str = typer.Option("ks_total_energy_ev", "--truth-energy-key"),
    candidate_energy_key: str = typer.Option("total_energy_ev", "--candidate-energy-key"),
    corrected_energy_key: str = typer.Option("corrected_total_energy_ev", "--corrected-energy-key"),
    delta_key: str = typer.Option("delta_energy_pred_ev", "--delta-key"),
) -> None:
    records = read_jsonl(dataset)
    result = run_delta_cv(
        records,
        folds=folds,
        ridge_alpha=ridge_alpha,
        truth_name=truth_name,
        raw_name=raw_name,
        delta_name=delta_name,
        truth_energy_key=truth_energy_key,
        candidate_energy_key=candidate_energy_key,
        corrected_energy_key=corrected_energy_key,
        delta_key=delta_key,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_dir / "usable_records.jsonl", result["usable_records"])
    write_jsonl(out_dir / "cv_raw.jsonl", result["raw_predictions"])
    write_jsonl(out_dir / "cv_delta_corrected.jsonl", result["delta_predictions"])
    (out_dir / "folds.json").write_text(
        json.dumps(result["folds"], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "benchmark.json").write_text(
        json.dumps(result["benchmark"], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "benchmark.md").write_text(render_benchmark_markdown(result["benchmark"]), encoding="utf-8")
    write_summary_csv(result["benchmark"], out_dir / "benchmark.csv")
    (out_dir / "cv_report.md").write_text(render_cv_report(result), encoding="utf-8")

    console.print(f"Usable records: {len(result['usable_records'])}")
    console.print(f"Folds: {len(result['folds'])}")
    console.print(f"Wrote delta CV outputs to {out_dir}")


def run_delta_cv(
    records: list[dict[str, Any]],
    folds: int,
    ridge_alpha: float,
    truth_name: str,
    raw_name: str,
    delta_name: str,
    truth_energy_key: str,
    candidate_energy_key: str,
    corrected_energy_key: str,
    delta_key: str,
) -> dict[str, Any]:
    usable = _usable_records(records, truth_energy_key=truth_energy_key, candidate_energy_key=candidate_energy_key)
    if len(usable) < 2:
        raise typer.BadParameter("At least two usable parsed_converged records are required for CV")
    actual_folds = min(folds, len(usable))
    fold_indices = _fold_indices(len(usable), actual_folds)
    raw_predictions = []
    delta_predictions = []
    fold_summaries = []

    for fold_index, test_indices in enumerate(fold_indices):
        test_index_set = set(test_indices)
        train_records = [record for index, record in enumerate(usable) if index not in test_index_set]
        test_records = [usable[index] for index in test_indices]
        if not train_records or not test_records:
            continue
        model, train_metrics = train_delta_model(
            train_records,
            ridge_alpha=ridge_alpha,
            truth_energy_key=truth_energy_key,
            candidate_energy_key=candidate_energy_key,
            corrected_energy_key=corrected_energy_key,
            delta_key=delta_key,
        )
        raw_fold = [_candidate_view(record, energy_key=candidate_energy_key) for record in test_records]
        delta_fold = [_candidate_view(record, energy_key=corrected_energy_key) for record in add_predictions(test_records, model)]
        raw_predictions.extend(raw_fold)
        delta_predictions.extend(delta_fold)
        fold_summaries.append(
            {
                "fold": fold_index,
                "n_train": len(train_records),
                "n_test": len(test_records),
                "test_structure_ids": [str(record.get("structure_id")) for record in test_records],
                "train_mae_ev": train_metrics["train_mae_ev"],
                "train_rmse_ev": train_metrics["train_rmse_ev"],
                "n_features": train_metrics["n_features"],
            }
        )

    benchmark = build_benchmark_report(
        usable,
        {
            raw_name: raw_predictions,
            delta_name: delta_predictions,
        },
        truth_name=truth_name,
    )
    return {
        "usable_records": usable,
        "raw_predictions": raw_predictions,
        "delta_predictions": delta_predictions,
        "folds": fold_summaries,
        "benchmark": benchmark,
        "settings": {
            "requested_folds": folds,
            "actual_folds": actual_folds,
            "ridge_alpha": ridge_alpha,
            "truth_name": truth_name,
            "truth_energy_key": truth_energy_key,
            "candidate_energy_key": candidate_energy_key,
            "corrected_energy_key": corrected_energy_key,
            "delta_key": delta_key,
        },
    }


def render_cv_report(result: dict[str, Any]) -> str:
    settings = result["settings"]
    lines = [
        "# Delta Cross-Validation Report",
        "",
        f"- Truth name: `{settings['truth_name']}`",
        f"- Usable records: {len(result['usable_records'])}",
        f"- Folds: {settings['actual_folds']} / requested {settings['requested_folds']}",
        f"- Ridge alpha: {settings['ridge_alpha']}",
        f"- Truth energy key: `{settings['truth_energy_key']}`",
        f"- Candidate energy key: `{settings['candidate_energy_key']}`",
        f"- Corrected energy key: `{settings['corrected_energy_key']}`",
        "",
        "## Fold Summary",
        "",
        "| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |",
        "| ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for fold in result["folds"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(fold["fold"]),
                    str(fold["n_train"]),
                    str(fold["n_test"]),
                    _fmt(fold["train_mae_ev"]),
                    _fmt(fold["train_rmse_ev"]),
                    ", ".join(fold["test_structure_ids"]),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Benchmark", "", render_benchmark_markdown(result["benchmark"])])
    return "\n".join(lines)


def _usable_records(
    records: list[dict[str, Any]],
    truth_energy_key: str,
    candidate_energy_key: str,
) -> list[dict[str, Any]]:
    usable = [
        record
        for record in records
        if record.get("ks_status") == "parsed_converged"
        and record.get("converged") is not False
        and record.get("candidate_converged") is not False
        and record.get(truth_energy_key) is not None
        and record.get(candidate_energy_key) is not None
    ]
    return sorted(usable, key=lambda record: str(record.get("structure_id", "")))


def _fold_indices(n_records: int, folds: int) -> list[list[int]]:
    groups = [[] for _ in range(folds)]
    for index in range(n_records):
        groups[index % folds].append(index)
    return [group for group in groups if group]


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
    if record.get("delta_adsorption_energy_pred_ev") is not None:
        candidate["delta_adsorption_energy_pred_ev"] = record.get("delta_adsorption_energy_pred_ev")
    return candidate


def _fmt(value: Any) -> str:
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


if __name__ == "__main__":
    app()
