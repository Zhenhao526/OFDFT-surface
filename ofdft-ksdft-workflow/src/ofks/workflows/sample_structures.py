from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import numpy as np
import typer
from ase.io import read, write
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl
from ofks.utils.hashing import get_structure_id

app = typer.Typer(help="Sample a diverse subset from an extxyz structure pool.")
console = Console()


@app.command()
def main(
    structures: Path = typer.Option(..., "--structures", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    max_count: int = typer.Option(..., "--max-count", min=1),
    records_out: Path | None = typer.Option(None, "--records-out", file_okay=True, dir_okay=False),
    exclude_records: list[Path] = typer.Option(
        [],
        "--exclude-records",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="JSONL records with structure_id to exclude. Can be repeated.",
    ),
    group_key: list[str] = typer.Option(
        ["site", "height_angstrom", "lateral_jitter_index"],
        "--group-key",
        help="Atoms.info key used for round-robin diversity. Can be repeated.",
    ),
) -> None:
    atoms_list = read(structures, ":")
    excluded = _excluded_ids(exclude_records)
    selected = sample_structures(atoms_list, max_count=max_count, excluded_ids=excluded, group_keys=group_key)
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, selected)
    if records_out is not None:
        write_jsonl(records_out, [_record(index, atoms) for index, atoms in enumerate(selected)])
    console.print(f"Selected {len(selected)} / {len(atoms_list)} structures")
    console.print(f"Wrote sampled structures to {out}")


def sample_structures(
    atoms_list,
    max_count: int,
    excluded_ids: set[str] | None = None,
    group_keys: list[str] | None = None,
):
    excluded_ids = excluded_ids or set()
    group_keys = group_keys or ["site", "height_angstrom", "lateral_jitter_index"]
    buckets: dict[tuple[str, ...], deque[Any]] = defaultdict(deque)
    seen: set[str] = set()
    for atoms in atoms_list:
        structure_id = get_structure_id(atoms)
        if structure_id in excluded_ids or structure_id in seen:
            continue
        seen.add(structure_id)
        buckets[_group(atoms, group_keys)].append(atoms)

    selected = []
    keys = sorted(buckets)
    while keys and len(selected) < max_count:
        next_keys = []
        for key in keys:
            if len(selected) >= max_count:
                break
            bucket = buckets[key]
            if not bucket:
                continue
            selected.append(bucket.popleft())
            if bucket:
                next_keys.append(key)
        keys = next_keys
    return selected


def _excluded_ids(paths: list[Path]) -> set[str]:
    ids: set[str] = set()
    for path in paths:
        for record in read_jsonl(path):
            structure_id = record.get("structure_id")
            if structure_id is not None:
                ids.add(str(structure_id))
    return ids


def _group(atoms, group_keys: list[str]) -> tuple[str, ...]:
    return tuple(str(atoms.info.get(key, "unknown")) for key in group_keys)


def _record(index: int, atoms) -> dict[str, Any]:
    return {
        "index": index,
        "structure_id": get_structure_id(atoms),
        "system_name": _jsonable(atoms.info.get("system_name")),
        "adsorbate": _jsonable(atoms.info.get("adsorbate")),
        "site": _jsonable(atoms.info.get("site")),
        "orientation": _jsonable(atoms.info.get("orientation")),
        "height_angstrom": _jsonable(atoms.info.get("height_angstrom")),
        "lateral_jitter_index": _jsonable(atoms.info.get("lateral_jitter_index")),
        "lateral_jitter_dx_angstrom": _jsonable(atoms.info.get("lateral_jitter_dx_angstrom")),
        "lateral_jitter_dy_angstrom": _jsonable(atoms.info.get("lateral_jitter_dy_angstrom")),
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    app()
