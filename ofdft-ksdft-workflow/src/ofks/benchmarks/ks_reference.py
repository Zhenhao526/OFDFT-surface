from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np


TRUTH_ENERGY_KEYS = ("ks_total_energy_ev", "total_energy_ev", "corrected_total_energy_ev")
CANDIDATE_ENERGY_KEYS = ("corrected_total_energy_ev", "total_energy_ev", "ks_total_energy_ev")
TRUTH_ADSORPTION_KEYS = ("ks_adsorption_energy_ev", "adsorption_energy_ev", "corrected_adsorption_energy_ev")
CANDIDATE_ADSORPTION_KEYS = ("corrected_adsorption_energy_ev", "adsorption_energy_ev", "ks_adsorption_energy_ev")
FORCE_KEYS = ("ks_forces_ev_per_ang", "forces_ev_per_ang")
MAX_FORCE_KEYS = ("ks_max_force_ev_per_ang", "max_force_ev_per_ang")
KS_RUNTIME_KEYS = ("qe_runtime_seconds", "ks_runtime_seconds")
CANDIDATE_RUNTIME_KEYS = ("qe_runtime_seconds", "ks_runtime_seconds", "runtime_seconds")


def build_benchmark_report(
    truth_records: list[dict[str, Any]],
    candidate_records_by_name: dict[str, list[dict[str, Any]]],
    truth_name: str = "ksdft",
) -> dict[str, Any]:
    truth_by_id = _index_by_structure_id(truth_records, energy_fn=_truth_energy)
    algorithms = []
    for name, candidate_records in candidate_records_by_name.items():
        algorithms.append(_benchmark_algorithm(name, candidate_records, truth_by_id))
    return {
        "truth_name": truth_name,
        "truth_records": len(truth_records),
        "truth_energy_records": sum(1 for record in truth_by_id.values() if _truth_energy(record) is not None),
        "algorithms": algorithms,
    }


def render_benchmark_markdown(report: dict[str, Any]) -> str:
    has_adsorption_metrics = any(
        algo.get("adsorption_energy_raw_mae_ev") is not None for algo in report["algorithms"]
    )
    lines = [
        f"# KSDFT Benchmark: {report['truth_name']}",
        "",
        f"- Truth records: {report['truth_records']}",
        f"- Truth records with energy: {report['truth_energy_records']}",
        "",
        "## Summary",
        "",
    ]
    if has_adsorption_metrics:
        lines.extend(
            [
                "| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
            ]
        )
    else:
        lines.extend(
            [
                "| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |",
                "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
            ]
        )
    for algo in report["algorithms"]:
        summary_values = [
            str(algo["name"]),
            str(algo["n_matched"]),
            _fmt(algo.get("energy_raw_mae_ev")),
            _fmt(algo.get("energy_aligned_mae_ev")),
        ]
        if has_adsorption_metrics:
            summary_values.extend(
                [
                    _fmt(algo.get("adsorption_energy_raw_mae_ev")),
                    _fmt(algo.get("adsorption_energy_aligned_mae_ev")),
                ]
            )
        summary_values.extend(
            [
                _fmt(_summary_value(algo, "spearman_energy", "adsorption_spearman_energy")),
                _top1_text(algo),
                _fmt(algo.get("candidate_runtime_total_seconds")),
                _fmt(algo.get("speedup_vs_truth")),
            ]
        )
        lines.append("| " + " | ".join(summary_values) + " |")
    lines.append("")
    lines.append("## Details")
    lines.append("")
    for algo in report["algorithms"]:
        lines.extend(_algorithm_detail_lines(algo))
    return "\n".join(lines)


def write_summary_csv(report: dict[str, Any], path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "name",
        "n_candidate_records",
        "n_matched",
        "energy_raw_mae_ev",
        "energy_raw_rmse_ev",
        "energy_aligned_mae_ev",
        "energy_aligned_rmse_ev",
        "adsorption_energy_raw_mae_ev",
        "adsorption_energy_raw_rmse_ev",
        "adsorption_energy_aligned_mae_ev",
        "adsorption_energy_aligned_rmse_ev",
        "adsorption_spearman_energy",
        "spearman_energy",
        "top1_match",
        "top3_recall",
        "candidate_converged_records",
        "matched_candidate_converged",
        "force_vector_mae_ev_per_ang",
        "max_force_mae_ev_per_ang",
        "candidate_runtime_total_seconds",
        "truth_runtime_total_seconds",
        "speedup_vs_truth",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for algo in report["algorithms"]:
            writer.writerow({key: algo.get(key) for key in fieldnames})


def _benchmark_algorithm(
    name: str,
    candidate_records: list[dict[str, Any]],
    truth_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    candidate_by_id = _index_by_structure_id(candidate_records, energy_fn=_candidate_energy)
    pairs = []
    for structure_id, truth in truth_by_id.items():
        candidate = candidate_by_id.get(structure_id)
        if candidate is None:
            continue
        pairs.append((structure_id, truth, candidate))

    truth_energies = []
    candidate_energies = []
    energy_ids = []
    for structure_id, truth, candidate in pairs:
        truth_energy = _truth_energy(truth)
        candidate_energy = _candidate_energy(candidate)
        if truth_energy is None or candidate_energy is None:
            continue
        energy_ids.append(structure_id)
        truth_energies.append(truth_energy)
        candidate_energies.append(candidate_energy)

    metrics: dict[str, Any] = {
        "name": name,
        "n_candidate_records": len(candidate_records),
        "candidate_converged_records": sum(1 for record in candidate_records if _is_converged(record)),
        "n_matched": len(pairs),
        "matched_candidate_converged": sum(1 for _, _, candidate in pairs if _is_converged(candidate)),
        "n_energy_pairs": len(energy_ids),
        "matched_structure_ids": [structure_id for structure_id, _, _ in pairs],
    }
    metrics.update(_energy_metrics(energy_ids, truth_energies, candidate_energies))
    metrics.update(_prefixed_energy_metrics("adsorption_", *_paired_values(pairs, _truth_adsorption_energy, _candidate_adsorption_energy)))
    metrics.update(_force_metrics(pairs))
    metrics.update(_runtime_metrics(pairs))
    return metrics


def _energy_metrics(
    structure_ids: list[str],
    truth_energies: list[float],
    candidate_energies: list[float],
) -> dict[str, Any]:
    if not truth_energies:
        return {}
    truth = np.asarray(truth_energies, dtype=float)
    candidate = np.asarray(candidate_energies, dtype=float)
    errors = candidate - truth
    offset = float(np.mean(errors))
    aligned_errors = errors - offset
    metrics = {
        "energy_raw_mae_ev": _mae(errors),
        "energy_raw_rmse_ev": _rmse(errors),
        "energy_raw_mean_signed_error_ev": offset,
        "energy_raw_max_abs_error_ev": _max_abs(errors),
        "energy_offset_ev": offset,
        "energy_aligned_mae_ev": _mae(aligned_errors),
        "energy_aligned_rmse_ev": _rmse(aligned_errors),
        "energy_aligned_max_abs_error_ev": _max_abs(aligned_errors),
        "spearman_energy": _spearman(truth, candidate),
        "top1_match": _topk_overlap(structure_ids, truth, candidate, k=1) == 1.0,
        "top3_recall": _topk_overlap(structure_ids, truth, candidate, k=3),
    }
    return metrics


def _prefixed_energy_metrics(
    prefix: str,
    structure_ids: list[str],
    truth_energies: list[float],
    candidate_energies: list[float],
) -> dict[str, Any]:
    metrics = _energy_metrics(structure_ids, truth_energies, candidate_energies)
    return {f"{prefix}{key}": value for key, value in metrics.items()}


def _paired_values(
    pairs: list[tuple[str, dict[str, Any], dict[str, Any]]],
    truth_fn,
    candidate_fn,
) -> tuple[list[str], list[float], list[float]]:
    structure_ids = []
    truth_values = []
    candidate_values = []
    for structure_id, truth, candidate in pairs:
        truth_value = truth_fn(truth)
        candidate_value = candidate_fn(candidate)
        if truth_value is None or candidate_value is None:
            continue
        structure_ids.append(structure_id)
        truth_values.append(truth_value)
        candidate_values.append(candidate_value)
    return structure_ids, truth_values, candidate_values


def _force_metrics(pairs: list[tuple[str, dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    vector_errors = []
    max_force_errors = []
    for _, truth, candidate in pairs:
        truth_forces = _forces(truth)
        candidate_forces = _forces(candidate)
        if truth_forces is not None and candidate_forces is not None and truth_forces.shape == candidate_forces.shape:
            norms = np.linalg.norm(candidate_forces - truth_forces, axis=1)
            vector_errors.extend(float(value) for value in norms)
        truth_max_force = _max_force(truth)
        candidate_max_force = _max_force(candidate)
        if truth_max_force is not None and candidate_max_force is not None:
            max_force_errors.append(candidate_max_force - truth_max_force)

    metrics: dict[str, Any] = {}
    if vector_errors:
        values = np.asarray(vector_errors, dtype=float)
        metrics["force_vector_mae_ev_per_ang"] = _mae(values)
        metrics["force_vector_rmse_ev_per_ang"] = _rmse(values)
    if max_force_errors:
        values = np.asarray(max_force_errors, dtype=float)
        metrics["max_force_mae_ev_per_ang"] = _mae(values)
        metrics["max_force_rmse_ev_per_ang"] = _rmse(values)
    return metrics


def _runtime_metrics(pairs: list[tuple[str, dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    truth_runtimes = [_truth_runtime(truth) for _, truth, _ in pairs]
    candidate_runtimes = [_candidate_runtime(candidate) for _, _, candidate in pairs]
    truth_values = [value for value in truth_runtimes if value is not None]
    candidate_values = [value for value in candidate_runtimes if value is not None]
    metrics: dict[str, Any] = {}
    if candidate_values:
        metrics["candidate_runtime_total_seconds"] = float(sum(candidate_values))
        metrics["candidate_runtime_median_seconds"] = float(median(candidate_values))
    if truth_values:
        metrics["truth_runtime_total_seconds"] = float(sum(truth_values))
        metrics["truth_runtime_median_seconds"] = float(median(truth_values))
    if truth_values and candidate_values and sum(candidate_values) > 0:
        metrics["speedup_vs_truth"] = float(sum(truth_values) / sum(candidate_values))
    return metrics


def _index_by_structure_id(
    records: list[dict[str, Any]],
    energy_fn,
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        structure_id = record.get("structure_id")
        if structure_id is None:
            continue
        key = str(structure_id)
        if key not in indexed or energy_fn(indexed[key]) is None:
            indexed[key] = record
    return indexed


def _truth_energy(record: dict[str, Any]) -> float | None:
    return _first_float(record, TRUTH_ENERGY_KEYS)


def _candidate_energy(record: dict[str, Any]) -> float | None:
    return _first_float(record, CANDIDATE_ENERGY_KEYS)


def _truth_adsorption_energy(record: dict[str, Any]) -> float | None:
    return _first_float(record, TRUTH_ADSORPTION_KEYS)


def _candidate_adsorption_energy(record: dict[str, Any]) -> float | None:
    return _first_float(record, CANDIDATE_ADSORPTION_KEYS)


def _max_force(record: dict[str, Any]) -> float | None:
    return _first_float(record, MAX_FORCE_KEYS)


def _truth_runtime(record: dict[str, Any]) -> float | None:
    return _first_float(record, KS_RUNTIME_KEYS)


def _candidate_runtime(record: dict[str, Any]) -> float | None:
    if record.get("ks_total_energy_ev") is not None:
        return _first_float(record, KS_RUNTIME_KEYS)
    return _first_float(record, CANDIDATE_RUNTIME_KEYS)


def _is_converged(record: dict[str, Any]) -> bool:
    return record.get("converged") is not False


def _forces(record: dict[str, Any]) -> np.ndarray | None:
    for key in FORCE_KEYS:
        value = record.get(key)
        if value is None:
            continue
        array = np.asarray(value, dtype=float)
        if array.ndim == 2 and array.shape[1] == 3:
            return array
    return None


def _first_float(record: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        value = record.get(key)
        if value is None:
            continue
        try:
            result = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(result):
            return result
    return None


def _mae(values: np.ndarray) -> float:
    return float(np.mean(np.abs(values)))


def _rmse(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(values * values)))


def _max_abs(values: np.ndarray) -> float:
    return float(np.max(np.abs(values)))


def _spearman(a: np.ndarray, b: np.ndarray) -> float | None:
    if a.size < 2:
        return None
    return _pearson(_rankdata(a), _rankdata(b))


def _pearson(a: np.ndarray, b: np.ndarray) -> float | None:
    centered_a = a - np.mean(a)
    centered_b = b - np.mean(b)
    denom = np.linalg.norm(centered_a) * np.linalg.norm(centered_b)
    if denom == 0:
        return None
    return float(np.dot(centered_a, centered_b) / denom)


def _rankdata(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(values.size, dtype=float)
    start = 0
    while start < values.size:
        end = start + 1
        while end < values.size and values[order[end]] == values[order[start]]:
            end += 1
        average_rank = 0.5 * (start + end - 1)
        ranks[order[start:end]] = average_rank
        start = end
    return ranks


def _topk_overlap(structure_ids: list[str], truth: np.ndarray, candidate: np.ndarray, k: int) -> float | None:
    if not structure_ids:
        return None
    limit = min(k, len(structure_ids))
    truth_top = {structure_ids[index] for index in np.argsort(truth)[:limit]}
    candidate_top = {structure_ids[index] for index in np.argsort(candidate)[:limit]}
    return float(len(truth_top & candidate_top) / limit)


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return str(value)
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def _top1_text(algo: dict[str, Any]) -> str:
    value = _summary_value(algo, "top1_match", "adsorption_top1_match")
    if value is None:
        return ""
    return "yes" if value else "no"


def _summary_value(algo: dict[str, Any], energy_key: str, adsorption_key: str) -> Any:
    value = algo.get(energy_key)
    if value is not None:
        return value
    return algo.get(adsorption_key)


def _algorithm_detail_lines(algo: dict[str, Any]) -> list[str]:
    lines = [
        f"### {algo['name']}",
        "",
        f"- Candidate records: {algo['n_candidate_records']}",
        f"- Candidate converged records: {algo.get('candidate_converged_records')}",
        f"- Matched records: {algo['n_matched']}",
        f"- Matched candidate converged records: {algo.get('matched_candidate_converged')}",
        f"- Energy pairs: {algo.get('n_energy_pairs', 0)}",
    ]
    detail_keys = [
        "energy_raw_mean_signed_error_ev",
        "energy_raw_max_abs_error_ev",
        "energy_offset_ev",
        "energy_aligned_max_abs_error_ev",
        "adsorption_energy_raw_mae_ev",
        "adsorption_energy_raw_rmse_ev",
        "adsorption_energy_raw_mean_signed_error_ev",
        "adsorption_energy_raw_max_abs_error_ev",
        "adsorption_energy_offset_ev",
        "adsorption_energy_aligned_mae_ev",
        "adsorption_energy_aligned_rmse_ev",
        "adsorption_energy_aligned_max_abs_error_ev",
        "adsorption_spearman_energy",
        "adsorption_top1_match",
        "adsorption_top3_recall",
        "force_vector_mae_ev_per_ang",
        "force_vector_rmse_ev_per_ang",
        "max_force_mae_ev_per_ang",
        "max_force_rmse_ev_per_ang",
        "candidate_runtime_median_seconds",
        "truth_runtime_median_seconds",
    ]
    for key in detail_keys:
        if algo.get(key) is not None:
            lines.append(f"- {key}: {_fmt(algo[key])}")
    if algo.get("matched_structure_ids"):
        lines.append(f"- Matched structure ids: {', '.join(algo['matched_structure_ids'][:10])}")
    lines.append("")
    return lines
