from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl

app = typer.Typer(help="Select the next KSDFT batch from fast-screen results.")
console = Console()


@app.command()
def main(
    pool: Path = typer.Option(..., "--pool", exists=True, file_okay=True, dir_okay=False),
    budget: int = typer.Option(30, "--budget", min=1),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    energy_key: str = typer.Option("total_energy_ev", "--energy-key"),
    exclude_records: list[Path] = typer.Option(
        [],
        "--exclude-records",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="JSONL records with structure_id to exclude. Can be repeated.",
    ),
) -> None:
    records = read_jsonl(pool)
    selected = select_records(records, budget=budget, energy_key=energy_key, excluded_ids=_excluded_ids(exclude_records))
    count = write_jsonl(out, selected)
    console.print(f"Wrote {count} selected records to {out}")


def select_records(
    records: list[dict[str, Any]],
    budget: int,
    energy_key: str = "total_energy_ev",
    excluded_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    excluded_ids = excluded_ids or set()
    valid = [
        record
        for record in records
        if record.get("converged")
        and record.get(energy_key) is not None
        and str(record.get("structure_id")) not in excluded_ids
    ]
    ranked = sorted(valid, key=lambda record: float(record[energy_key]))
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    seen_groups: set[tuple[str, str]] = set()

    for record in ranked:
        group = _diversity_group(record)
        if group in seen_groups:
            continue
        _append_selected(selected, selected_ids, record, energy_key, "best_in_site_orientation_group")
        seen_groups.add(group)
        if len(selected) >= budget:
            return selected

    for record in ranked:
        _append_selected(selected, selected_ids, record, energy_key, "low_energy_fill")
        if len(selected) >= budget:
            return selected

    return selected


def _append_selected(
    selected: list[dict[str, Any]],
    selected_ids: set[str],
    record: dict[str, Any],
    energy_key: str,
    reason: str,
) -> None:
    structure_id = str(record.get("structure_id"))
    if structure_id in selected_ids:
        return
    enriched = dict(record)
    enriched["selection_rank"] = len(selected)
    enriched["selection_reason"] = reason
    enriched["selection_score_ev"] = float(record[energy_key])
    selected.append(enriched)
    selected_ids.add(structure_id)


def _diversity_group(record: dict[str, Any]) -> tuple[str, str]:
    return (str(record.get("site", "unknown")), str(record.get("orientation", "unknown")))


def _excluded_ids(paths: list[Path]) -> set[str]:
    ids: set[str] = set()
    for path in paths:
        for record in read_jsonl(path):
            structure_id = record.get("structure_id")
            if structure_id is not None:
                ids.add(str(structure_id))
    return ids


if __name__ == "__main__":
    app()
