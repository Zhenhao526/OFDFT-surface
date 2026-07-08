from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl
from ofks.metrics.adsorption import adsorption_energy

app = typer.Typer(help="Build adsorption-energy records from mixed OFDFT component calculations.")
console = Console()


@app.command()
def main(
    adsorbed: Path = typer.Option(..., "--adsorbed", exists=True, file_okay=True, dir_okay=False),
    slab_reference: Path = typer.Option(..., "--slab-reference", exists=True, file_okay=True, dir_okay=False),
    adsorbate_reference: Path = typer.Option(..., "--adsorbate-reference", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    candidate_name: str = typer.Option("hybrid_ofdft", "--candidate-name"),
    backend: str = typer.Option("hybrid_ofdft", "--backend"),
    adsorbed_source: str = typer.Option("adsorbed", "--adsorbed-source"),
    slab_source: str = typer.Option("slab", "--slab-source"),
    adsorbate_source: str = typer.Option("adsorbate", "--adsorbate-source"),
    energy_key: str = typer.Option("total_energy_ev", "--energy-key"),
    slab_energy_key: str = typer.Option("total_energy_ev", "--slab-energy-key"),
    adsorbate_energy_key: str = typer.Option("total_energy_ev", "--adsorbate-energy-key"),
    slab_reference_kind: str | None = typer.Option("clean_slab", "--slab-reference-kind"),
    adsorbate_reference_kind: str | None = typer.Option("isolated_adsorbate", "--adsorbate-reference-kind"),
    slab_reference_id: str | None = typer.Option(None, "--slab-reference-id"),
    adsorbate_reference_id: str | None = typer.Option(None, "--adsorbate-reference-id"),
) -> None:
    records = build_hybrid_adsorption_records(
        adsorbed_records=read_jsonl(adsorbed),
        slab_reference_records=read_jsonl(slab_reference),
        adsorbate_reference_records=read_jsonl(adsorbate_reference),
        candidate_name=candidate_name,
        backend=backend,
        adsorbed_source=adsorbed_source,
        slab_source=slab_source,
        adsorbate_source=adsorbate_source,
        energy_key=energy_key,
        slab_energy_key=slab_energy_key,
        adsorbate_energy_key=adsorbate_energy_key,
        slab_reference_kind=slab_reference_kind,
        adsorbate_reference_kind=adsorbate_reference_kind,
        slab_reference_id=slab_reference_id,
        adsorbate_reference_id=adsorbate_reference_id,
    )
    count = write_jsonl(out, records)
    console.print(f"Wrote {count} hybrid adsorption records to {out}")


def build_hybrid_adsorption_records(
    adsorbed_records: list[dict[str, Any]],
    slab_reference_records: list[dict[str, Any]],
    adsorbate_reference_records: list[dict[str, Any]],
    *,
    candidate_name: str,
    backend: str,
    adsorbed_source: str,
    slab_source: str,
    adsorbate_source: str,
    energy_key: str = "total_energy_ev",
    slab_energy_key: str = "total_energy_ev",
    adsorbate_energy_key: str = "total_energy_ev",
    slab_reference_kind: str | None = "clean_slab",
    adsorbate_reference_kind: str | None = "isolated_adsorbate",
    slab_reference_id: str | None = None,
    adsorbate_reference_id: str | None = None,
) -> list[dict[str, Any]]:
    slab = select_reference_record(
        slab_reference_records,
        reference_kind=slab_reference_kind,
        reference_id=slab_reference_id,
        role="slab",
    )
    adsorbate = select_reference_record(
        adsorbate_reference_records,
        reference_kind=adsorbate_reference_kind,
        reference_id=adsorbate_reference_id,
        role="adsorbate",
    )
    slab_energy = _required_energy(slab, slab_energy_key, role="slab")
    adsorbate_energy = _required_energy(adsorbate, adsorbate_energy_key, role="adsorbate")

    hybrid_records = []
    for record in adsorbed_records:
        if energy_key not in record or record[energy_key] is None:
            continue
        adsorbed_energy = float(record[energy_key])
        item = _candidate_record_view(record)
        item.update(
            {
                "backend": backend,
                "candidate_name": candidate_name,
                "total_energy_ev": adsorbed_energy,
                "adsorption_energy_ev": adsorption_energy(adsorbed_energy, slab_energy, adsorbate_energy),
                "converged": _combined_convergence(record, slab, adsorbate),
                "runtime_seconds": _combined_runtime(record, slab, adsorbate),
                "metadata": _hybrid_metadata(
                    record=record,
                    slab=slab,
                    adsorbate=adsorbate,
                    adsorbed_source=adsorbed_source,
                    slab_source=slab_source,
                    adsorbate_source=adsorbate_source,
                    energy_key=energy_key,
                    slab_energy_key=slab_energy_key,
                    adsorbate_energy_key=adsorbate_energy_key,
                    adsorbed_energy=adsorbed_energy,
                    slab_energy=slab_energy,
                    adsorbate_energy=adsorbate_energy,
                ),
            }
        )
        hybrid_records.append(item)
    return hybrid_records


def select_reference_record(
    records: list[dict[str, Any]],
    *,
    reference_kind: str | None,
    reference_id: str | None,
    role: str,
) -> dict[str, Any]:
    candidates = records
    if reference_kind is not None:
        candidates = [record for record in candidates if record.get("reference_kind") == reference_kind]
    if reference_id is not None:
        candidates = [record for record in candidates if record.get("reference_id") == reference_id]
    if len(candidates) != 1:
        selector = []
        if reference_kind is not None:
            selector.append(f"reference_kind={reference_kind!r}")
        if reference_id is not None:
            selector.append(f"reference_id={reference_id!r}")
        selector_text = ", ".join(selector) or "single-record input"
        raise ValueError(f"Expected exactly one {role} reference matching {selector_text}; found {len(candidates)}.")
    return candidates[0]


def _required_energy(record: dict[str, Any], key: str, *, role: str) -> float:
    value = record.get(key)
    if value is None:
        raise ValueError(f"Missing {role} reference energy key {key!r}.")
    return float(value)


def _candidate_record_view(record: dict[str, Any]) -> dict[str, Any]:
    keep_keys = [
        "index",
        "structure_id",
        "system_name",
        "adsorbate",
        "site",
        "orientation",
        "height_angstrom",
        "max_force_ev_per_ang",
        "forces_ev_per_ang",
    ]
    return {key: record.get(key) for key in keep_keys if key in record}


def _combined_convergence(*records: dict[str, Any]) -> bool | None:
    values = [record.get("converged") for record in records]
    if any(value is False for value in values):
        return False
    if all(value is True for value in values):
        return True
    return None


def _combined_runtime(*records: dict[str, Any]) -> float | None:
    runtimes = [record.get("runtime_seconds") for record in records]
    if any(value is None for value in runtimes):
        return None
    return float(sum(float(value) for value in runtimes))


def _component_metadata(record: dict[str, Any], *, source: str, role: str, energy_key: str, energy: float) -> dict[str, Any]:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    return {
        "role": role,
        "source": source,
        "backend": record.get("backend"),
        "candidate_name": record.get("candidate_name"),
        "structure_id": record.get("structure_id"),
        "reference_kind": record.get("reference_kind"),
        "reference_id": record.get("reference_id"),
        "energy_key": energy_key,
        "total_energy_ev": energy,
        "converged": record.get("converged"),
        "runtime_seconds": record.get("runtime_seconds"),
        "kedf": metadata.get("kedf"),
        "xc": metadata.get("xc"),
    }


def _hybrid_metadata(
    *,
    record: dict[str, Any],
    slab: dict[str, Any],
    adsorbate: dict[str, Any],
    adsorbed_source: str,
    slab_source: str,
    adsorbate_source: str,
    energy_key: str,
    slab_energy_key: str,
    adsorbate_energy_key: str,
    adsorbed_energy: float,
    slab_energy: float,
    adsorbate_energy: float,
) -> dict[str, Any]:
    return {
        "hybrid_formula": "E_ads = E(slab+adsorbate) - E(clean_slab) - E(adsorbate)",
        "components": {
            "adsorbed": _component_metadata(
                record,
                source=adsorbed_source,
                role="adsorbed",
                energy_key=energy_key,
                energy=adsorbed_energy,
            ),
            "slab": _component_metadata(
                slab,
                source=slab_source,
                role="clean_slab",
                energy_key=slab_energy_key,
                energy=slab_energy,
            ),
            "adsorbate": _component_metadata(
                adsorbate,
                source=adsorbate_source,
                role="adsorbate",
                energy_key=adsorbate_energy_key,
                energy=adsorbate_energy,
            ),
        },
    }


if __name__ == "__main__":
    app()
