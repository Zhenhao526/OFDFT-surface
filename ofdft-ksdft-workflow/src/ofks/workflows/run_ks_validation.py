from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import typer
from ase import Atoms
from ase.io import read, write
from rich.console import Console

from ofks.calculators.qe_input import render_qe_input
from ofks.config import load_yaml
from ofks.io import read_jsonl, write_jsonl
from ofks.utils.hashing import get_structure_id

app = typer.Typer(help="Prepare KSDFT validation calculation folders.")
console = Console()


@app.command()
def main(
    selected: Path = typer.Option(..., "--selected", exists=True, file_okay=True, dir_okay=False),
    structures: Path = typer.Option(..., "--structures", exists=True, file_okay=True, dir_okay=False),
    calculator: Path = typer.Option(..., "--calculator", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=False, dir_okay=True),
) -> None:
    selected_records = read_jsonl(selected)
    atoms_list = read(structures, index=":")
    config = load_yaml(calculator)
    records = prepare_ks_validation_batch(selected_records, atoms_list, config, out)
    manifest = out / "manifest.jsonl"
    count = write_jsonl(manifest, records)
    console.print(f"Prepared {count} KSDFT input folders under {out}")
    console.print(f"Wrote manifest to {manifest}")


def prepare_ks_validation_batch(
    selected_records: list[dict[str, Any]],
    atoms_list: list[Atoms],
    calculator_config: dict[str, Any],
    output_dir: str | Path,
) -> list[dict[str, Any]]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    structures_by_id = _index_structures(atoms_list)
    prepared: list[dict[str, Any]] = []
    for fallback_rank, record in enumerate(selected_records):
        structure_id = str(record.get("structure_id"))
        if structure_id not in structures_by_id:
            raise KeyError(f"Selected structure not found in structure file: {structure_id}")
        atoms = structures_by_id[structure_id]
        rank = int(record.get("selection_rank", fallback_rank))
        job_dir = out / f"{rank:04d}_{structure_id}"
        job_dir.mkdir(parents=True, exist_ok=True)
        prefix = _qe_prefix(record, rank)
        qe_input = render_qe_input(atoms, calculator_config, prefix=prefix)
        input_path = job_dir / "pw.in"
        structure_path = job_dir / "structure.extxyz"
        metadata_path = job_dir / "metadata.json"
        input_path.write_text(qe_input, encoding="utf-8")
        atoms_to_write = atoms.copy()
        atoms_to_write.info.pop("adsorbate_info", None)
        write(structure_path, atoms_to_write)
        metadata_path.write_text(json.dumps(_jsonable(record), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        prepared.append(
            {
                **record,
                "ks_backend": calculator_config.get("backend"),
                "ks_input": str(input_path),
                "ks_structure": str(structure_path),
                "ks_metadata": str(metadata_path),
                "ks_job_dir": str(job_dir),
                "ks_status": "input_prepared",
            }
        )
    return prepared


def _index_structures(atoms_list: list[Atoms]) -> dict[str, Atoms]:
    indexed: dict[str, Atoms] = {}
    for atoms in atoms_list:
        structure_id = get_structure_id(atoms)
        indexed[structure_id] = atoms
    return indexed


def _qe_prefix(record: dict[str, Any], rank: int) -> str:
    system = str(record.get("system_name") or "system")
    structure_id = str(record.get("structure_id") or "structure")
    return f"{system}_{rank:04d}_{structure_id}"


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    app()
