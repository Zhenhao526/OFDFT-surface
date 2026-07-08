from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl

app = typer.Typer(help="Merge candidate algorithm outputs into parsed KSDFT truth labels by structure_id.")
console = Console()


@app.command()
def main(
    truth: Path = typer.Option(..., "--truth", exists=True, file_okay=True, dir_okay=False),
    candidate: Path = typer.Option(..., "--candidate", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    candidate_name: str = typer.Option("candidate", "--candidate-name"),
) -> None:
    merged = merge_candidate_labels(read_jsonl(truth), read_jsonl(candidate), candidate_name=candidate_name)
    count = write_jsonl(out, merged)
    console.print(f"Wrote {count} merged candidate-label records to {out}")


def merge_candidate_labels(
    truth_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
    candidate_name: str,
) -> list[dict[str, Any]]:
    candidate_by_id = {
        str(record["structure_id"]): record for record in candidate_records if record.get("structure_id") is not None
    }
    merged = []
    for truth in truth_records:
        structure_id = truth.get("structure_id")
        if structure_id is None:
            continue
        candidate = candidate_by_id.get(str(structure_id))
        if candidate is None:
            continue
        record = dict(truth)
        record.update(
            {
                "backend": candidate.get("backend"),
                "candidate_name": candidate_name,
                "candidate_converged": candidate.get("converged"),
                "candidate_metadata": candidate.get("metadata"),
                "total_energy_ev": candidate.get("total_energy_ev"),
                "adsorption_energy_ev": candidate.get("adsorption_energy_ev"),
                "forces_ev_per_ang": candidate.get("forces_ev_per_ang"),
                "max_force_ev_per_ang": candidate.get("max_force_ev_per_ang"),
                "runtime_seconds": candidate.get("runtime_seconds"),
            }
        )
        merged.append(record)
    return merged


if __name__ == "__main__":
    app()
