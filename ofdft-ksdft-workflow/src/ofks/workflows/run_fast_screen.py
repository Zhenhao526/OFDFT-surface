from __future__ import annotations

from pathlib import Path

import typer
from ase.io import read
from rich.console import Console

from ofks.calculators import build_calculator
from ofks.io import write_jsonl
from ofks.utils.hashing import get_structure_id

app = typer.Typer(help="Run fast screening calculations for candidate structures.")
console = Console()


@app.command()
def main(
    structures: Path = typer.Option(..., "--structures", exists=True, file_okay=True, dir_okay=False),
    calculator: Path = typer.Option(..., "--calculator", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
) -> None:
    runner = build_calculator(calculator)
    atoms_list = read(structures, index=":")
    records = []
    for index, atoms in enumerate(atoms_list):
        structure_id = get_structure_id(atoms)
        result = runner.calculate(atoms)
        records.append(
            {
                "index": index,
                "structure_id": structure_id,
                "system_name": atoms.info.get("system_name"),
                "reference_kind": atoms.info.get("reference_kind"),
                "reference_id": atoms.info.get("reference_id"),
                "adsorbate": atoms.info.get("adsorbate"),
                "site": atoms.info.get("site"),
                "orientation": atoms.info.get("orientation"),
                "height_angstrom": atoms.info.get("height_angstrom"),
                "backend": result.backend,
                "converged": result.converged,
                "total_energy_ev": result.total_energy_ev,
                "max_force_ev_per_ang": result.max_force_ev_per_ang,
                "runtime_seconds": result.runtime_seconds,
                "metadata": result.metadata,
            }
        )
    count = write_jsonl(out, records)
    console.print(f"Wrote {count} fast-screen records to {out}")


if __name__ == "__main__":
    app()
