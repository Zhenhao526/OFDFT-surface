from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl
from ofks.parsers.qe import parse_qe_output

app = typer.Typer(help="Parse KSDFT output files and update workflow records.")
console = Console()


@app.command()
def main(
    manifest: Path = typer.Option(..., "--manifest", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    output_name: str = typer.Option("pw.out", "--output-name"),
    overlay: list[Path] = typer.Option(
        [],
        "--overlay",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Optional JSONL run-result records to overlay by structure_id before parsing.",
    ),
) -> None:
    records = read_jsonl(manifest)
    if overlay:
        records = overlay_records_by_structure_id(records, [read_jsonl(path) for path in overlay])
    parsed = parse_ks_manifest(records, output_name=output_name)
    count = write_jsonl(out, parsed)
    parsed_count = sum(1 for record in parsed if record.get("ks_status") == "parsed_converged")
    missing_count = sum(1 for record in parsed if record.get("ks_status") == "output_missing")
    console.print(f"Wrote {count} parsed records to {out}")
    console.print(f"Parsed converged: {parsed_count}; missing outputs: {missing_count}")


def parse_ks_manifest(records: list[dict[str, Any]], output_name: str = "pw.out") -> list[dict[str, Any]]:
    parsed_records = []
    for record in records:
        enriched = dict(record)
        output_path = _resolve_output_path(record, output_name)
        enriched["ks_output"] = str(output_path)
        if not output_path.exists():
            enriched["ks_status"] = "output_missing"
            parsed_records.append(enriched)
            continue
        try:
            result = parse_qe_output(output_path)
        except Exception as exc:  # pragma: no cover - defensive status for production runs
            enriched["ks_status"] = "parse_failed"
            enriched["ks_parse_error"] = str(exc)
            parsed_records.append(enriched)
            continue
        inconsistency = _parse_inconsistency(record, result)
        if inconsistency is not None:
            enriched.update(
                {
                    "ks_status": "parse_inconsistent",
                    "ks_converged": False,
                    "ks_job_done": result.job_done,
                    "ks_parse_inconsistency": inconsistency,
                }
            )
            parsed_records.append(enriched)
            continue
        enriched.update(
            {
                "ks_status": "parsed_converged" if result.converged else "parsed_unconverged",
                "ks_converged": result.converged,
                "ks_job_done": result.job_done,
                "ks_total_energy_ev": result.total_energy_ev,
                "ks_total_energy_ry": result.raw_total_energy_ry,
                "ks_max_force_ev_per_ang": result.max_force_ev_per_ang,
                "ks_forces_ev_per_ang": None
                if result.forces_ev_per_ang is None
                else _jsonable(result.forces_ev_per_ang),
            }
        )
        parsed_records.append(enriched)
    return parsed_records


def _parse_inconsistency(record: dict[str, Any], result: Any) -> str | None:
    expected_atoms = _expected_atom_count(record)
    if expected_atoms is None or result.forces_ev_per_ang is None:
        return None
    parsed_forces = int(result.forces_ev_per_ang.shape[0])
    if parsed_forces != expected_atoms:
        return f"force_count_mismatch: parsed {parsed_forces} forces for {expected_atoms} atoms"
    return None


def _expected_atom_count(record: dict[str, Any]) -> int | None:
    structure_path = record.get("ks_structure")
    if structure_path is None:
        return None
    path = Path(str(structure_path))
    if not path.exists():
        return None
    from ase.io import read

    return len(read(path))


def overlay_records_by_structure_id(
    records: list[dict[str, Any]],
    overlays: list[list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    overlay_by_id: dict[str, dict[str, Any]] = {}
    for overlay_records in overlays:
        for record in overlay_records:
            structure_id = record.get("structure_id")
            if structure_id is not None:
                overlay_by_id[str(structure_id)] = record
    merged = []
    for record in records:
        structure_id = record.get("structure_id")
        overlay = overlay_by_id.get(str(structure_id)) if structure_id is not None else None
        merged.append({**record, **overlay} if overlay is not None else dict(record))
    return merged


def _resolve_output_path(record: dict[str, Any], output_name: str) -> Path:
    if record.get("ks_output"):
        return Path(str(record["ks_output"]))
    return Path(str(record["ks_job_dir"])) / output_name


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    app()
