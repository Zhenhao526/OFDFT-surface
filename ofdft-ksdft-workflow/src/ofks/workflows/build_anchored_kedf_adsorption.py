from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console

from ofks.benchmarks import build_benchmark_report, render_benchmark_markdown, write_summary_csv
from ofks.io import read_jsonl, write_jsonl
from ofks.workflows.build_fixed_o_kedf_benchmark import (
    _adsorption_sign_sanity,
    _candidate_view,
    _combined_convergence,
    _combined_runtime,
    _component_summary,
    _dedupe_by_structure_id,
    _fmt,
    _load_named_records,
    _parse_named_paths,
    _required_energy,
    _runtime_with_reference_share,
    _select_clean_slab,
)

app = typer.Typer(help="Benchmark KEDF adsorption energies with a per-KEDF KS-anchor mu_O calibration.")
console = Console()


@app.command()
def main(
    truth: Path = typer.Option(..., "--truth", exists=True, file_okay=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False, dir_okay=True),
    candidate: Annotated[
        list[str],
        typer.Option("--candidate", help="KEDF adsorbed records as variant=path. Repeat to merge paths."),
    ] = [],
    slab_reference: Annotated[
        list[str],
        typer.Option("--slab-reference", help="KEDF clean-slab records as variant=path. Repeat to merge paths."),
    ] = [],
    anchor_structure_id: str = typer.Option("f67b4fe8525ec26c", "--anchor-structure-id"),
    clean_slab_id: str = typer.Option("d78831db0d40c74b", "--clean-slab-id"),
    truth_adsorption_key: str = typer.Option("ks_adsorption_energy_ev", "--truth-adsorption-key"),
    truth_name: str = typer.Option("ksdft_anchored_mu_o", "--truth-name"),
) -> None:
    candidate_paths = _parse_named_paths(candidate, role="candidate")
    slab_reference_paths = _parse_named_paths(slab_reference, role="slab-reference")
    truth_records = read_jsonl(truth)
    result = build_anchored_kedf_adsorption_records(
        truth_records=truth_records,
        candidate_records_by_name=_load_named_records(candidate_paths),
        slab_reference_records_by_name=_load_named_records(slab_reference_paths),
        anchor_structure_id=anchor_structure_id,
        clean_slab_id=clean_slab_id,
        truth_adsorption_key=truth_adsorption_key,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    candidate_dir = out_dir / "candidates"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    candidate_files = {}
    for name, records in result["candidates"].items():
        path = candidate_dir / f"{name}_ks_anchor_mu_o.jsonl"
        write_jsonl(path, records)
        candidate_files[name] = str(path)

    report = build_benchmark_report(truth_records, result["candidates"], truth_name=truth_name)
    (out_dir / "benchmark.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "benchmark.md").write_text(render_benchmark_markdown(report), encoding="utf-8")
    write_summary_csv(report, out_dir / "benchmark.csv")

    sign_sanity = _adsorption_sign_sanity(result["candidates"])
    manifest = {
        "candidate_files": candidate_files,
        "clean_slab_id": clean_slab_id,
        "anchor": result["anchor"],
        "calibrations": result["calibrations"],
        "adsorption_sign_sanity": sign_sanity,
        "expansion_gate": _expansion_gate(sign_sanity, skipped=result["skipped"]),
        "skipped": result["skipped"],
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "anchored_kedf_adsorption_report.md").write_text(
        render_anchored_kedf_report(report, manifest),
        encoding="utf-8",
    )

    console.print(f"Wrote KS-anchor KEDF benchmark to {out_dir}")


def build_anchored_kedf_adsorption_records(
    *,
    truth_records: list[dict[str, Any]],
    candidate_records_by_name: dict[str, list[dict[str, Any]]],
    slab_reference_records_by_name: dict[str, list[dict[str, Any]]],
    anchor_structure_id: str,
    clean_slab_id: str,
    truth_adsorption_key: str = "ks_adsorption_energy_ev",
) -> dict[str, Any]:
    anchor_truth = _select_truth_record(truth_records, anchor_structure_id=anchor_structure_id)
    if anchor_truth is None:
        raise ValueError(f"Missing KS anchor truth structure_id={anchor_structure_id}.")
    anchor_truth_adsorption = _required_energy(
        anchor_truth,
        truth_adsorption_key,
        role=f"KS anchor {anchor_structure_id}",
    )

    output: dict[str, list[dict[str, Any]]] = {}
    calibrations: dict[str, dict[str, Any]] = {}
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
        anchor_record = _select_structure(energy_records, structure_id=anchor_structure_id)
        if anchor_record is None:
            skipped.append({"variant": name, "reason": f"missing anchor adsorbed structure_id={anchor_structure_id}"})
            continue

        anchor_adsorbed_energy = _required_energy(anchor_record, "total_energy_ev", role=f"{name} anchor adsorbed")
        anchor_delta = anchor_adsorbed_energy - slab_energy
        mu_o_eff = anchor_delta - anchor_truth_adsorption
        reference_runtime = _combined_runtime(slab)
        reference_runtime_share = (
            reference_runtime / len(energy_records) if reference_runtime is not None and energy_records else None
        )

        records = []
        for record in energy_records:
            adsorbed_energy = _required_energy(record, "total_energy_ev", role=f"{name} adsorbed")
            delta_interface = adsorbed_energy - slab_energy
            item = _candidate_view(record)
            item.update(
                {
                    "backend": "dftpy",
                    "candidate_name": f"{name}_ks_anchor_mu_o",
                    "variant": name,
                    "total_energy_ev": adsorbed_energy,
                    "adsorption_energy_ev": delta_interface - mu_o_eff,
                    "converged": _combined_convergence(record, slab),
                    "runtime_seconds": _runtime_with_reference_share(record, reference_runtime_share),
                    "metadata": {
                        "ks_anchor_calibration": True,
                        "hybrid_formula": (
                            "Delta_i = E_KEDF(slab+O_i) - E_KEDF(clean_slab); "
                            "mu_O_eff = Delta_anchor - E_ads_KS(anchor); "
                            "E_ads_pred(i) = Delta_i - mu_O_eff"
                        ),
                        "kedf_variant": name,
                        "delta_interface_energy_ev": delta_interface,
                        "mu_o_eff_ev": mu_o_eff,
                        "anchor": {
                            "structure_id": anchor_structure_id,
                            "truth_adsorption_energy_ev": anchor_truth_adsorption,
                            "adsorbed_total_energy_ev": anchor_adsorbed_energy,
                            "clean_slab_total_energy_ev": slab_energy,
                            "delta_interface_energy_ev": anchor_delta,
                        },
                        "reference_runtime_seconds": reference_runtime,
                        "reference_runtime_amortized_seconds": reference_runtime_share,
                        "adsorbed": _component_summary(record, role="adsorbed"),
                        "slab": _component_summary(slab, role="clean_slab"),
                    },
                }
            )
            records.append(item)
        output[name] = records
        calibrations[name] = {
            "anchor_structure_id": anchor_structure_id,
            "truth_adsorption_energy_ev": anchor_truth_adsorption,
            "clean_slab_structure_id": clean_slab_id,
            "clean_slab_total_energy_ev": slab_energy,
            "anchor_adsorbed_total_energy_ev": anchor_adsorbed_energy,
            "anchor_delta_interface_energy_ev": anchor_delta,
            "mu_o_eff_ev": mu_o_eff,
            "candidate_records": len(records),
        }

    return {
        "anchor": {
            "structure_id": anchor_structure_id,
            "truth_adsorption_key": truth_adsorption_key,
            "truth_adsorption_energy_ev": anchor_truth_adsorption,
            "site": anchor_truth.get("site"),
            "height_angstrom": anchor_truth.get("height_angstrom"),
            "system_name": anchor_truth.get("system_name"),
        },
        "candidates": output,
        "calibrations": calibrations,
        "skipped": skipped,
    }


def render_anchored_kedf_report(report: dict[str, Any], manifest: dict[str, Any]) -> str:
    anchor = manifest["anchor"]
    lines = [
        "# KS-Anchor KEDF Adsorption Benchmark",
        "",
        "This benchmark replaces the fixed absolute atomic-O reference with a per-KEDF effective oxygen chemical potential calibrated to one KSDFT adsorption anchor:",
        "",
        "```text",
        "Delta_i(KEDF) = E_KEDF(Mg slab + O_i) - E_KEDF(clean Mg slab)",
        "mu_O_eff(KEDF) = Delta_anchor(KEDF) - E_ads_KS(anchor)",
        "E_ads_pred(i) = Delta_i(KEDF) - mu_O_eff(KEDF)",
        "```",
        "",
        "This removes the inconsistent absolute O-energy zero from the mixed KEDF/M-OFDFT branch. The remaining first4 test checks whether the KEDF relative interface-energy landscape is physically usable.",
        "",
        "## KS Anchor",
        "",
        f"- structure_id: `{anchor['structure_id']}`",
        f"- truth adsorption key: `{anchor['truth_adsorption_key']}`",
        f"- KS adsorption energy: `{_fmt(anchor['truth_adsorption_energy_ev'])}` eV",
        f"- site/height: `{anchor.get('site')}` / `{_fmt(anchor.get('height_angstrom'))}` A",
        "",
    ]

    calibrations = manifest.get("calibrations") or {}
    if calibrations:
        lines.extend(
            [
                "## Effective mu_O",
                "",
                "| variant | records | anchor Delta(eV) | KS anchor Eads(eV) | mu_O_eff(eV) |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for name, item in calibrations.items():
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{name}`",
                        str(item["candidate_records"]),
                        _fmt(item["anchor_delta_interface_energy_ev"]),
                        _fmt(item["truth_adsorption_energy_ev"]),
                        _fmt(item["mu_o_eff_ev"]),
                    ]
                )
                + " |"
            )
        lines.append("")

    sign_sanity = manifest.get("adsorption_sign_sanity") or {}
    if sign_sanity:
        lines.extend(
            [
                "## Adsorption Sign Sanity",
                "",
                "For atomic O adsorption on Mg(0001), the KSDFT references in this benchmark are negative. The first4 branch is eligible for 12-structure expansion only when calibrated adsorption energies stay negative.",
                "",
                "| variant | records | negative Eads | nonnegative Eads | min Eads(eV) | max Eads(eV) | first4 gate |",
                "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for name, item in sign_sanity.items():
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{name}`",
                        str(item["records"]),
                        str(item["negative_records"]),
                        str(item["nonnegative_records"]),
                        _fmt(item["min_adsorption_energy_ev"]),
                        _fmt(item["max_adsorption_energy_ev"]),
                        "pass" if item["all_negative"] else "block 12",
                    ]
                )
                + " |"
            )
        lines.append("")

    gate = manifest.get("expansion_gate") or {}
    if gate:
        lines.extend(
            [
                "## Expansion Gate",
                "",
                f"- passed: `{gate['passed']}`",
                f"- passed variants: `{', '.join(gate['passed_variants']) if gate['passed_variants'] else 'none'}`",
                f"- blocked variants: `{', '.join(gate['blocked_variants']) if gate['blocked_variants'] else 'none'}`",
            ]
        )
        if not gate["passed"]:
            lines.append("- decision: 12-structure expansion is blocked until the first4 sign sanity check passes.")
        lines.append("")

    lines.extend(["## Benchmark", "", render_benchmark_markdown(report)])
    if manifest["skipped"]:
        lines.extend(["", "## Skipped Variants", ""])
        for item in manifest["skipped"]:
            lines.append(f"- `{item['variant']}`: {item['reason']}")
    return "\n".join(lines) + "\n"


def _select_truth_record(records: list[dict[str, Any]], *, anchor_structure_id: str) -> dict[str, Any] | None:
    return _select_structure(records, structure_id=anchor_structure_id)


def _select_structure(records: list[dict[str, Any]], *, structure_id: str) -> dict[str, Any] | None:
    for record in records:
        if record.get("structure_id") == structure_id:
            return record
    return None


def _expansion_gate(sign_sanity: dict[str, dict[str, Any]], *, skipped: list[dict[str, str]] | None = None) -> dict[str, Any]:
    skipped = skipped or []
    passed_variants = [
        name for name, item in sign_sanity.items() if item.get("records", 0) > 0 and item.get("all_negative") is True
    ]
    blocked_variants = [
        name for name, item in sign_sanity.items() if item.get("records", 0) == 0 or item.get("all_negative") is not True
    ]
    blocked_variants.extend(item["variant"] for item in skipped)
    return {
        "criterion": "all requested variants must complete and all calibrated first4 adsorption_energy_ev values must be < 0 before expanding to 12 structures",
        "passed": bool(sign_sanity) and not blocked_variants and not skipped,
        "passed_variants": passed_variants,
        "blocked_variants": blocked_variants,
    }


if __name__ == "__main__":
    app()
