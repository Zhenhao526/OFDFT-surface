from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from ase import Atoms
from ase.io import write
from rich.console import Console

from ofks.config import SystemConfig, load_system_config
from ofks.io import write_jsonl
from ofks.structures.adsorbates import build_adsorbate
from ofks.structures.slabs import build_slab
from ofks.utils.hashing import structure_hash

app = typer.Typer(help="Generate clean-slab and isolated-adsorbate reference structures.")
console = Console()


@app.command()
def main(
    system: Path = typer.Option(..., "--system", exists=True, file_okay=True, dir_okay=False),
    structures_out: Path = typer.Option(..., "--structures-out", file_okay=True, dir_okay=False),
    records_out: Path = typer.Option(..., "--records-out", file_okay=True, dir_okay=False),
    molecule_box_angstrom: float = typer.Option(12.0, "--molecule-box-angstrom", min=4.0),
) -> None:
    config = load_system_config(system)
    atoms_list, records = generate_reference_structures(config, molecule_box_angstrom=molecule_box_angstrom)
    structures_out.parent.mkdir(parents=True, exist_ok=True)
    write(structures_out, atoms_list)
    count = write_jsonl(records_out, records)
    console.print(f"Wrote {len(atoms_list)} reference structures to {structures_out}")
    console.print(f"Wrote {count} reference records to {records_out}")


def generate_reference_structures(
    config: SystemConfig,
    molecule_box_angstrom: float = 12.0,
) -> tuple[list[Atoms], list[dict[str, Any]]]:
    slab = build_slab(
        element=config.surface.element,
        miller=config.surface.miller,
        size=config.surface.size,
        vacuum=config.surface.vacuum_angstrom,
        fixed_layers=config.surface.fixed_layers,
    )
    slab.info.update(
        {
            "system_name": config.name,
            "reference_kind": "clean_slab",
            "adsorbate": "none",
            "reference_id": config.references.get("slab_id", f"{config.name}_clean_slab"),
        }
    )
    slab.info.pop("adsorbate_info", None)
    slab.info["structure_id"] = structure_hash(slab)

    adsorbate = build_adsorbate(config.adsorbate.name)
    adsorbate.set_cell([molecule_box_angstrom, molecule_box_angstrom, molecule_box_angstrom])
    adsorbate.set_pbc([True, True, True])
    adsorbate.center()
    adsorbate.info.update(
        {
            "system_name": config.name,
            "reference_kind": "isolated_adsorbate",
            "adsorbate": config.adsorbate.name,
            "reference_id": config.references.get("adsorbate_id", f"{config.name}_{config.adsorbate.name}"),
            "molecule_box_angstrom": float(molecule_box_angstrom),
        }
    )
    adsorbate.info["structure_id"] = structure_hash(adsorbate)
    adsorbate.info.pop("adsorbate_info", None)

    atoms_list = [slab, adsorbate]
    records = [_reference_record(index, atoms) for index, atoms in enumerate(atoms_list)]
    return atoms_list, records


def _reference_record(index: int, atoms: Atoms) -> dict[str, Any]:
    return {
        "index": index,
        "selection_rank": index,
        "structure_id": atoms.info["structure_id"],
        "system_name": atoms.info.get("system_name"),
        "reference_kind": atoms.info.get("reference_kind"),
        "reference_id": atoms.info.get("reference_id"),
        "adsorbate": atoms.info.get("adsorbate"),
        "molecule_box_angstrom": atoms.info.get("molecule_box_angstrom"),
    }


if __name__ == "__main__":
    app()
