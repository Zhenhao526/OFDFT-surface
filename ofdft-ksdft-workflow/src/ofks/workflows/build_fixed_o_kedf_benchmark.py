from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console

from ofks.benchmarks import build_benchmark_report, render_benchmark_markdown, write_summary_csv
from ofks.io import read_jsonl, write_jsonl
from ofks.metrics.adsorption import adsorption_energy

app = typer.Typer(help="Benchmark KEDF interface energies with a fixed atomic-O reference.")
console = Console()


@app.command()
def main(
    truth: Path = typer.Option(..., "--truth", exists=True, file_okay=True, dir_okay=False),
    adsorbate_reference: Path = typer.Option(..., "--adsorbate-reference", exists=True, file_okay=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False, dir_okay=True),
    candidate: Annotated[
        list[str],
        typer.Option("--candidate", help="KEDF adsorbed records as variant=path. Repeat to merge paths."),
    ] = [],
    slab_reference: Annotated[
        list[str],
        typer.Option("--slab-reference", help="KEDF reference records as variant=path. Repeat to merge paths."),
    ] = [],
    clean_slab_id: str = typer.Option("d78831db0d40c74b", "--clean-slab-id"),
    truth_name: str = typer.Option("ksdft_fixed_o", "--truth-name"),
) -> None:
    candidate_paths = _parse_named_paths(candidate, role="candidate")
    slab_reference_paths = _parse_named_paths(slab_reference, role="slab-reference")
    adsorbate_reference_records = read_jsonl(adsorbate_reference)
    if len(adsorbate_reference_records) != 1:
        raise typer.BadParameter("adsorbate-reference must contain exactly one record.")

    result = build_fixed_o_kedf_benchmark_records(
        candidate_records_by_name=_load_named_records(candidate_paths),
        slab_reference_records_by_name=_load_named_records(slab_reference_paths),
        adsorbate_reference_record=adsorbate_reference_records[0],
        clean_slab_id=clean_slab_id,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    candidate_dir = out_dir / "candidates"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    candidate_files = {}
    for name, records in result["candidates"].items():
        path = candidate_dir / f"{name}_fixed_o.jsonl"
        write_jsonl(path, records)
        candidate_files[name] = str(path)

    report = build_benchmark_report(read_jsonl(truth), result["candidates"], truth_name=truth_name)
    (out_dir / "benchmark.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    (out_dir / "benchmark.md").write_text(render_benchmark_markdown(report), encoding="utf-8")
    write_summary_csv(report, out_dir / "benchmark.csv")

    manifest = {
        "candidate_files": candidate_files,
        "clean_slab_id": clean_slab_id,
        "adsorbate_reference": _component_summary(adsorbate_reference_records[0]),
        "skipped": result["skipped"],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "fixed_o_kedf_interface_report.md").write_text(
        render_fixed_o_report(report, manifest),
        encoding="utf-8",
    )

    console.print(f"Wrote fixed-O KEDF benchmark to {out_dir}")


def build_fixed_o_kedf_benchmark_records(
    *,
    candidate_records_by_name: dict[str, list[dict[str, Any]]],
    slab_reference_records_by_name: dict[str, list[dict[str, Any]]],
    adsorbate_reference_record: dict[str, Any],
    clean_slab_id: str,
) -> dict[str, Any]:
    adsorbate_energy = _required_energy(adsorbate_reference_record, "total_energy_ev", role="adsorbate")
    output: dict[str, list[dict[str, Any]]] = {}
    skipped: list[dict[str, str]] = []

    for name, adsorbed_records in candidate_records_by_name.items():
        slab_records = slab_reference_records_by_name.get(name)
        if slab_records is None:
            skipped.append({"variant": name, "reason": "missing slab-reference input"})
            continue
        slab = _select_clean_slab(slab_records, clean_slab_id=clean_slab_id)
        if slab is None:
            skipped.append({"variant": name, "reason": f"missing clean slab structure_id={clean_slab_id}"})
            continue
        slab_energy = _required_energy(slab, "total_energy_ev", role=f"{name} slab")
        deduped = _dedupe_by_structure_id(adsorbed_records)
        energy_records = [record for record in deduped if record.get("total_energy_ev") is not None]
        reference_runtime = _combined_runtime(slab, adsorbate_reference_record)
        reference_runtime_share = (
            reference_runtime / len(energy_records) if reference_runtime is not None and energy_records else None
        )
        records = []
        for record in energy_records:
            energy = record.get("total_energy_ev")
            adsorbed_energy = float(energy)
            item = _candidate_view(record)
            item.update(
                {
                    "backend": "dftpy",
                    "candidate_name": f"{name}_fixed_o",
                    "variant": name,
                    "total_energy_ev": adsorbed_energy,
                    "adsorption_energy_ev": adsorption_energy(adsorbed_energy, slab_energy, adsorbate_energy),
                    "converged": _combined_convergence(record, slab, adsorbate_reference_record),
                    "runtime_seconds": _runtime_with_reference_share(record, reference_runtime_share),
                    "metadata": {
                        "fixed_o_reference": True,
                        "hybrid_formula": "E_ads = E_KEDF(slab+O) - E_KEDF(clean_slab) - E_fixed(O)",
                        "kedf_variant": name,
                        "reference_runtime_seconds": reference_runtime,
                        "reference_runtime_amortized_seconds": reference_runtime_share,
                        "adsorbed": _component_summary(record, role="adsorbed"),
                        "slab": _component_summary(slab, role="clean_slab"),
                        "adsorbate": _component_summary(adsorbate_reference_record, role="adsorbate"),
                    },
                }
            )
            records.append(item)
        output[name] = records
    return {"candidates": output, "skipped": skipped}


def render_fixed_o_report(report: dict[str, Any], manifest: dict[str, Any]) -> str:
    lines = [
        "# Fixed Atomic-O KEDF Interface Benchmark",
        "",
        "This benchmark uses one calibrated atomic-O reference for every KEDF variant:",
        "",
        "```text",
        "E_ads = E_KEDF(Mg slab + O) - E_KEDF(clean Mg slab) - E_fixed(O)",
        "```",
        "",
        "The goal is to focus the comparison on the adsorbed Mg+O and clean-slab KEDF energies after the atomic-O reference has been fixed.",
        "",
        "Caveat: current KEDF coverage is still sparse. Four-structure pilot metrics are useful for screening obvious failures and offsets, but ranking conclusions require more completed slab+adsorbed pairs.",
        "",
        "## Adsorbate Reference",
        "",
        f"- reference_id: `{manifest['adsorbate_reference'].get('reference_id')}`",
        f"- total_energy_ev: `{manifest['adsorbate_reference'].get('total_energy_ev')}`",
        "",
        "## Benchmark",
        "",
        render_benchmark_markdown(report),
    ]
    if manifest["skipped"]:
        lines.extend(["", "## Skipped Variants", ""])
        for item in manifest["skipped"]:
            lines.append(f"- `{item['variant']}`: {item['reason']}")
    return "\n".join(lines) + "\n"


def _parse_named_paths(items: list[str], *, role: str) -> dict[str, list[Path]]:
    if not items:
        raise typer.BadParameter(f"Provide at least one --{role} variant=path")
    paths: dict[str, list[Path]] = {}
    for item in items:
        if "=" not in item:
            raise typer.BadParameter(f"{role} must be variant=path, got: {item}")
        name, raw_path = item.split("=", 1)
        name = name.strip()
        path = Path(raw_path.strip())
        if not name:
            raise typer.BadParameter(f"{role} variant is empty: {item}")
        if not path.exists():
            raise typer.BadParameter(f"{role} file does not exist: {path}")
        paths.setdefault(name, []).append(path)
    return paths


def _load_named_records(paths_by_name: dict[str, list[Path]]) -> dict[str, list[dict[str, Any]]]:
    records_by_name = {}
    for name, paths in paths_by_name.items():
        records = []
        for path in paths:
            records.extend(read_jsonl(path))
        records_by_name[name] = records
    return records_by_name


def _dedupe_by_structure_id(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for record in records:
        structure_id = record.get("structure_id")
        if not structure_id:
            continue
        if structure_id not in deduped:
            deduped[str(structure_id)] = record
    return list(deduped.values())


def _select_clean_slab(records: list[dict[str, Any]], *, clean_slab_id: str) -> dict[str, Any] | None:
    matches = [record for record in records if record.get("structure_id") == clean_slab_id]
    if not matches:
        return None
    return matches[0]


def _required_energy(record: dict[str, Any], key: str, *, role: str) -> float:
    value = record.get(key)
    if value is None:
        raise ValueError(f"Missing {role} energy key {key!r}.")
    return float(value)


def _candidate_view(record: dict[str, Any]) -> dict[str, Any]:
    keep_keys = [
        "structure_index",
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
    available = [float(value) for value in runtimes if value is not None]
    if not available:
        return None
    return float(sum(available))


def _runtime_with_reference_share(record: dict[str, Any], reference_runtime_share: float | None) -> float | None:
    values = []
    runtime = record.get("runtime_seconds")
    if runtime is not None:
        values.append(float(runtime))
    if reference_runtime_share is not None:
        values.append(float(reference_runtime_share))
    if not values:
        return None
    return float(sum(values))


def _component_summary(record: dict[str, Any], *, role: str | None = None) -> dict[str, Any]:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    return {
        "role": role,
        "variant": record.get("variant"),
        "structure_id": record.get("structure_id"),
        "reference_id": record.get("reference_id"),
        "reference_kind": record.get("reference_kind"),
        "total_energy_ev": record.get("total_energy_ev"),
        "converged": record.get("converged"),
        "runtime_seconds": record.get("runtime_seconds"),
        "kedf": metadata.get("kedf"),
        "xc": metadata.get("xc"),
    }


if __name__ == "__main__":
    app()
