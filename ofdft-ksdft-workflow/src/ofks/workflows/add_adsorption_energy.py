from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl
from ofks.metrics.adsorption import adsorption_energy

app = typer.Typer(help="Add adsorption-energy fields to records from slab and adsorbate references.")
console = Console()


@app.command()
def main(
    records: Path = typer.Option(..., "--records", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    slab_energy_ev: float = typer.Option(..., "--slab-energy-ev"),
    adsorbate_energy_ev: float = typer.Option(..., "--adsorbate-energy-ev"),
    energy_key: str = typer.Option("ks_total_energy_ev", "--energy-key"),
    out_key: str = typer.Option("ks_adsorption_energy_ev", "--out-key"),
) -> None:
    updated = add_adsorption_energy_fields(
        read_jsonl(records),
        slab_energy_ev=slab_energy_ev,
        adsorbate_energy_ev=adsorbate_energy_ev,
        energy_key=energy_key,
        out_key=out_key,
    )
    count = write_jsonl(out, updated)
    console.print(f"Wrote {count} records with adsorption energies to {out}")


def add_adsorption_energy_fields(
    records: list[dict[str, Any]],
    slab_energy_ev: float,
    adsorbate_energy_ev: float,
    energy_key: str,
    out_key: str,
) -> list[dict[str, Any]]:
    updated = []
    for record in records:
        copy = dict(record)
        energy = copy.get(energy_key)
        if energy is not None:
            copy[out_key] = adsorption_energy(float(energy), slab_energy_ev, adsorbate_energy_ev)
        updated.append(copy)
    return updated


if __name__ == "__main__":
    app()
