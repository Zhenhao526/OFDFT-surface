from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import typer
from ase.io import read
from rich.console import Console

from ofks.calculators.dftpy_runner import DftpyCalculatorRunner
from ofks.config import load_yaml
from ofks.utils.hashing import get_structure_id

app = typer.Typer(help="Sweep small DFTpy convergence settings before production OFDFT benchmarks.")
console = Console()


SWEEP_VARIANTS: list[dict[str, Any]] = [
    {
        "name": "wt_heg_sp08_m30",
        "updates": {
            "kedf": "WT",
            "density_initial": "heg",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "wt_heg_sp08_m100",
        "updates": {
            "kedf": "WT",
            "density_initial": "heg",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 100, "maxfun": 100, "econv": 1.0e-5},
        },
    },
    {
        "name": "wt_heg_sp10_m100",
        "updates": {
            "kedf": "WT",
            "density_initial": "heg",
            "grid_spacing_angstrom": 1.0,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 100, "maxfun": 100, "econv": 1.0e-5},
        },
    },
    {
        "name": "wt_atomic_sp08_m100",
        "updates": {
            "kedf": "WT",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 100, "maxfun": 100, "econv": 1.0e-5},
        },
    },
    {
        "name": "mgp_atomic_sp08_m30",
        "updates": {
            "kedf": "MGP",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "mgpa_atomic_sp08_m30",
        "updates": {
            "kedf": "MGPA",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "lmgp_atomic_sp08_m30",
        "updates": {
            "kedf": "LMGP",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "lmgpa_atomic_sp08_m30",
        "updates": {
            "kedf": "LMGPA",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "hc_atomic_sp08_m30",
        "updates": {
            "kedf": "HC",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "revhc_atomic_sp08_m30",
        "updates": {
            "kedf": "revHC",
            "density_initial": "atomic",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 30, "maxfun": 30, "econv": 1.0e-5},
        },
    },
    {
        "name": "tfvw_heg_sp08_m100",
        "updates": {
            "kedf": "TFvW",
            "density_initial": "heg",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 100, "maxfun": 100, "econv": 1.0e-5},
        },
    },
    {
        "name": "tf_heg_sp08_m100",
        "updates": {
            "kedf": "TF",
            "density_initial": "heg",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "CG-HS", "algorithm": "EMM", "maxiter": 100, "maxfun": 100, "econv": 1.0e-5},
        },
    },
    {
        "name": "wt_lbfgs_sp08_m100",
        "updates": {
            "kedf": "WT",
            "density_initial": "heg",
            "grid_spacing_angstrom": 0.8,
            "optimization": {"method": "LBFGS", "algorithm": "EMM", "maxiter": 100, "maxfun": 100, "econv": 1.0e-5},
        },
    },
]


@app.command()
def main(
    structures: Path = typer.Option(..., "--structures", exists=True, file_okay=True, dir_okay=False),
    calculator: Path = typer.Option(..., "--calculator", exists=True, file_okay=True, dir_okay=False),
    out_jsonl: Path = typer.Option(..., "--out-jsonl", file_okay=True, dir_okay=False),
    out_md: Path | None = typer.Option(None, "--out-md", file_okay=True, dir_okay=False),
    structure_limit: int = typer.Option(1, "--structure-limit", min=1),
    variant_filter: str | None = typer.Option(
        None,
        "--variant-filter",
        help="Comma-separated sweep variant names to run. Defaults to all variants.",
    ),
) -> None:
    base_config = load_yaml(calculator)
    atoms_list = read(structures, index=":")[:structure_limit]
    variants = filter_sweep_variants(variant_filter)
    records = []
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_jsonl.open("w", encoding="utf-8") as handle:
        for structure_index, atoms in enumerate(atoms_list):
            for variant in variants:
                config = _merged_config(base_config, variant["updates"])
                config["quiet"] = True
                runner = DftpyCalculatorRunner(config)
                record = {
                    "structure_index": structure_index,
                    "structure_id": get_structure_id(atoms),
                    "site": atoms.info.get("site"),
                    "height_angstrom": atoms.info.get("height_angstrom"),
                    "variant": variant["name"],
                    "config": _config_summary(config),
                }
                try:
                    result = runner.calculate(atoms)
                    record.update(
                        {
                            "status": "ok",
                            "converged": result.converged,
                            "total_energy_ev": result.total_energy_ev,
                            "max_force_ev_per_ang": result.max_force_ev_per_ang,
                            "runtime_seconds": result.runtime_seconds,
                            "metadata": result.metadata,
                        }
                    )
                except Exception as exc:  # noqa: BLE001 - sweep should record failed variants and continue.
                    record.update({"status": "error", "error_type": type(exc).__name__, "error": str(exc)})
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                handle.flush()
                records.append(record)

    count = len(records)
    if out_md is not None:
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_sweep_markdown(records), encoding="utf-8")
    console.print(f"Wrote {count} DFTpy sweep records to {out_jsonl}")


def filter_sweep_variants(variant_filter: str | None) -> list[dict[str, Any]]:
    if not variant_filter:
        return SWEEP_VARIANTS
    requested = [name.strip() for name in variant_filter.split(",") if name.strip()]
    available = {variant["name"]: variant for variant in SWEEP_VARIANTS}
    missing = [name for name in requested if name not in available]
    if missing:
        raise typer.BadParameter(
            "Unknown sweep variant(s): "
            + ", ".join(missing)
            + ". Available variants: "
            + ", ".join(available)
        )
    return [available[name] for name in requested]


def render_sweep_markdown(records: list[dict[str, Any]]) -> str:
    lines = [
        "# DFTpy Convergence Sweep",
        "",
        f"- Records: {len(records)}",
        f"- OK records: {sum(1 for record in records if record.get('status') == 'ok')}",
        f"- Converged records: {sum(1 for record in records if record.get('converged') is True)}",
        "",
        "| variant | structure_id | site | h(A) | status | converged | iterations | E(eV) | Fmax(eV/A) | runtime(s) |",
        "| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for record in records:
        metadata = record.get("metadata") or {}
        lines.append(
            "| "
            + " | ".join(
                [
                    str(record.get("variant", "")),
                    str(record.get("structure_id", "")),
                    str(record.get("site", "")),
                    _fmt(record.get("height_angstrom")),
                    str(record.get("status", "")),
                    _yes_no(record.get("converged")),
                    _fmt(metadata.get("density_iterations")),
                    _fmt(record.get("total_energy_ev")),
                    _fmt(record.get("max_force_ev_per_ang")),
                    _fmt(record.get("runtime_seconds")),
                ]
            )
            + " |"
        )
    errors = [record for record in records if record.get("status") == "error"]
    if errors:
        lines.extend(["", "## Errors", ""])
        for record in errors:
            lines.append(f"- {record.get('variant')}: {record.get('error_type')} - {record.get('error')}")
    return "\n".join(lines)


def _merged_config(base_config: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base_config)
    _deep_update(result, updates)
    return result


def _deep_update(target: dict[str, Any], updates: dict[str, Any]) -> None:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = copy.deepcopy(value)


def _config_summary(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "kedf": config.get("kedf"),
        "xc": config.get("xc"),
        "density_initial": config.get("density_initial"),
        "grid_spacing_angstrom": config.get("grid_spacing_angstrom"),
        "optimization": config.get("optimization"),
    }


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def _yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return ""


if __name__ == "__main__":
    app()
