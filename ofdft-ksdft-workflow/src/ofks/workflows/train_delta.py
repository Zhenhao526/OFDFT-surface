from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl
from ofks.models.delta import train_delta_model

app = typer.Typer(help="Train a baseline delta-learning model from parsed KSDFT labels.")
console = Console()


@app.command()
def main(
    dataset: Path = typer.Option(..., "--dataset", exists=True, file_okay=True, dir_okay=False),
    model_out: Path = typer.Option(..., "--model-out", file_okay=True, dir_okay=False),
    report: Path = typer.Option(..., "--report", file_okay=True, dir_okay=False),
    predictions_out: Path | None = typer.Option(None, "--predictions-out", file_okay=True, dir_okay=False),
    ridge_alpha: float = typer.Option(1.0, "--ridge-alpha", min=0.0),
) -> None:
    records = read_jsonl(dataset)
    model, metrics = train_delta_model(records, ridge_alpha=ridge_alpha)
    model.save(model_out)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render_report(metrics, model_out), encoding="utf-8")
    if predictions_out is not None:
        predictions = add_predictions(records, model)
        write_jsonl(predictions_out, predictions)
    console.print(f"Wrote delta model to {model_out}")
    console.print(f"Wrote training report to {report}")


def add_predictions(records: list[dict[str, Any]], model) -> list[dict[str, Any]]:
    predictions = model.predict(records)
    enriched = []
    for record, delta in zip(records, predictions):
        item = dict(record)
        item[model.delta_key] = float(delta)
        if item.get(model.candidate_energy_key) is not None:
            item[model.corrected_energy_key] = float(item[model.candidate_energy_key]) + float(delta)
        enriched.append(item)
    return enriched


def render_report(metrics: dict[str, Any], model_path: Path) -> str:
    lines = [
        "# Delta-Learning Baseline Report",
        "",
        f"- Model: `{model_path}`",
        f"- Trainable records: {metrics['n_records_trainable']} / {metrics['n_records_total']}",
        f"- Features: {metrics['n_features']}",
        f"- Ridge alpha: {metrics['ridge_alpha']}",
        f"- Target mean delta energy: {metrics['target_mean_ev']:.8f} eV",
        f"- Truth energy key: `{metrics.get('truth_energy_key', 'ks_total_energy_ev')}`",
        f"- Candidate energy key: `{metrics.get('candidate_energy_key', 'total_energy_ev')}`",
        f"- Corrected energy key: `{metrics.get('corrected_energy_key', 'corrected_total_energy_ev')}`",
        f"- Train MAE: {metrics['train_mae_ev']:.8f} eV",
        f"- Train RMSE: {metrics['train_rmse_ev']:.8f} eV",
    ]
    if metrics.get("warning"):
        lines.extend(["", f"Warning: {metrics['warning']}"])
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    app()
