from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import write_jsonl

app = typer.Typer(help="Build an energy-only reference record from an external method.")
console = Console()


@app.command()
def main(
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    energy_ev: float = typer.Option(..., "--energy-ev"),
    reference_id: str = typer.Option(..., "--reference-id"),
    adsorbate: str = typer.Option("O", "--adsorbate"),
    formula: str = typer.Option("O", "--formula"),
    energy_scale: float = typer.Option(1.0, "--energy-scale"),
    energy_shift_ev: float = typer.Option(0.0, "--energy-shift-ev"),
    reference_kind: str = typer.Option("isolated_adsorbate", "--reference-kind"),
    system_name: str | None = typer.Option(None, "--system-name"),
    backend: str = typer.Option("mofdft", "--backend"),
    candidate_name: str = typer.Option("mofdft_reference", "--candidate-name"),
    method: str | None = typer.Option(None, "--method"),
    xc: str | None = typer.Option(None, "--xc"),
    reference_convention: str | None = typer.Option(None, "--reference-convention"),
    structure_id: str | None = typer.Option(None, "--structure-id"),
    runtime_seconds: float | None = typer.Option(None, "--runtime-seconds"),
    converged: bool = typer.Option(True, "--converged/--not-converged"),
) -> None:
    record = build_reference_energy_record(
        energy_ev=energy_ev,
        reference_id=reference_id,
        adsorbate=adsorbate,
        formula=formula,
        energy_scale=energy_scale,
        energy_shift_ev=energy_shift_ev,
        reference_kind=reference_kind,
        system_name=system_name,
        backend=backend,
        candidate_name=candidate_name,
        method=method,
        xc=xc,
        reference_convention=reference_convention,
        structure_id=structure_id,
        runtime_seconds=runtime_seconds,
        converged=converged,
    )
    count = write_jsonl(out, [record])
    console.print(f"Wrote {count} reference energy record to {out}")


def build_reference_energy_record(
    *,
    energy_ev: float,
    reference_id: str,
    adsorbate: str = "O",
    formula: str = "O",
    energy_scale: float = 1.0,
    energy_shift_ev: float = 0.0,
    reference_kind: str = "isolated_adsorbate",
    system_name: str | None = None,
    backend: str = "mofdft",
    candidate_name: str = "mofdft_reference",
    method: str | None = None,
    xc: str | None = None,
    reference_convention: str | None = None,
    structure_id: str | None = None,
    runtime_seconds: float | None = None,
    converged: bool = True,
) -> dict[str, Any]:
    scaled_energy_ev = float(energy_ev) * float(energy_scale)
    total_energy_ev = scaled_energy_ev + float(energy_shift_ev)
    metadata = _drop_none(
        {
            "source": "external_reference_energy",
            "formula": formula,
            "input_energy_ev": float(energy_ev),
            "energy_scale": float(energy_scale),
            "scaled_energy_ev": scaled_energy_ev,
            "energy_shift_ev": float(energy_shift_ev),
            "method": method,
            "xc": xc,
            "reference_convention": reference_convention,
        }
    )
    return _drop_none(
        {
            "index": 0,
            "structure_id": structure_id,
            "system_name": system_name,
            "reference_kind": reference_kind,
            "reference_id": reference_id,
            "adsorbate": adsorbate,
            "backend": backend,
            "candidate_name": candidate_name,
            "total_energy_ev": total_energy_ev,
            "converged": converged,
            "runtime_seconds": runtime_seconds,
            "metadata": metadata,
        }
    )


def _drop_none(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if value is not None}


if __name__ == "__main__":
    app()
