from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ase.io import read

from ofks.io import read_jsonl


@dataclass(frozen=True)
class WorkflowSummary:
    system: str
    counts: dict[str, int | float | str | None] = field(default_factory=dict)
    status_counts: dict[str, dict[str, int]] = field(default_factory=dict)
    top_fast: list[dict[str, Any]] = field(default_factory=list)
    top_corrected: list[dict[str, Any]] = field(default_factory=list)
    delta_report_excerpt: str | None = None
    recommendations: list[str] = field(default_factory=list)


def build_summary(
    system: str,
    candidates: str | Path | None = None,
    fast_screen: str | Path | None = None,
    selected: str | Path | None = None,
    manifest: str | Path | None = None,
    parsed: str | Path | None = None,
    predictions: str | Path | None = None,
    delta_report: str | Path | None = None,
) -> WorkflowSummary:
    counts: dict[str, int | float | str | None] = {}
    status_counts: dict[str, dict[str, int]] = {}
    top_fast: list[dict[str, Any]] = []
    top_corrected: list[dict[str, Any]] = []

    if candidates:
        counts["candidate_structures"] = _count_structures(candidates)

    fast_records = _read_if_present(fast_screen)
    if fast_records is not None:
        counts["fast_screen_records"] = len(fast_records)
        counts["fast_screen_converged"] = sum(1 for record in fast_records if record.get("converged"))
        top_fast = _top_records(fast_records, "total_energy_ev")

    selected_records = _read_if_present(selected)
    if selected_records is not None:
        counts["selected_records"] = len(selected_records)
        status_counts["selection_reason"] = dict(Counter(str(record.get("selection_reason")) for record in selected_records))

    manifest_records = _read_if_present(manifest)
    if manifest_records is not None:
        counts["ks_manifest_records"] = len(manifest_records)
        status_counts["manifest_status"] = dict(Counter(str(record.get("ks_status")) for record in manifest_records))

    parsed_records = _read_if_present(parsed)
    if parsed_records is not None:
        counts["parsed_records"] = len(parsed_records)
        ks_status = Counter(str(record.get("ks_status")) for record in parsed_records)
        status_counts["parsed_status"] = dict(ks_status)
        counts["parsed_converged"] = ks_status.get("parsed_converged", 0)
        counts["output_missing"] = ks_status.get("output_missing", 0)

    prediction_records = _read_if_present(predictions)
    if prediction_records is not None:
        counts["prediction_records"] = len(prediction_records)
        counts["corrected_energy_records"] = sum(
            1 for record in prediction_records if record.get("corrected_total_energy_ev") is not None
        )
        top_corrected = _top_records(prediction_records, "corrected_total_energy_ev")

    delta_excerpt = None
    if delta_report and Path(delta_report).exists():
        delta_excerpt = _read_excerpt(delta_report)

    recommendations = _recommend(counts)
    return WorkflowSummary(
        system=system,
        counts=counts,
        status_counts=status_counts,
        top_fast=top_fast,
        top_corrected=top_corrected,
        delta_report_excerpt=delta_excerpt,
        recommendations=recommendations,
    )


def render_summary_markdown(summary: WorkflowSummary) -> str:
    lines = [f"# Workflow Summary: {summary.system}", ""]
    lines.extend(["## Counts", ""])
    if summary.counts:
        for key in sorted(summary.counts):
            lines.append(f"- {key}: {summary.counts[key]}")
    else:
        lines.append("- No count data available.")
    lines.append("")

    if summary.status_counts:
        lines.extend(["## Status Counts", ""])
        for name, counts in summary.status_counts.items():
            lines.append(f"### {name}")
            for key, value in sorted(counts.items()):
                lines.append(f"- {key}: {value}")
            lines.append("")

    lines.extend(["## Top Fast-Screen Records", ""])
    lines.extend(_render_table(summary.top_fast, "total_energy_ev"))
    lines.append("")

    lines.extend(["## Top Corrected Records", ""])
    lines.extend(_render_table(summary.top_corrected, "corrected_total_energy_ev"))
    lines.append("")

    if summary.delta_report_excerpt:
        lines.extend(["## Delta Report Excerpt", "", summary.delta_report_excerpt.strip(), ""])

    lines.extend(["## Recommendations", ""])
    for item in summary.recommendations:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def _count_structures(path: str | Path) -> int:
    structures = read(path, index=":")
    return len(structures)


def _read_if_present(path: str | Path | None) -> list[dict[str, Any]] | None:
    if path is None:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    return read_jsonl(candidate)


def _top_records(records: list[dict[str, Any]], energy_key: str, limit: int = 5) -> list[dict[str, Any]]:
    valid = [record for record in records if record.get(energy_key) is not None]
    ranked = sorted(valid, key=lambda record: float(record[energy_key]))
    keys = ["structure_id", "site", "orientation", "height_angstrom", energy_key, "ks_status"]
    return [{key: record.get(key) for key in keys if key in record} for record in ranked[:limit]]


def _render_table(records: list[dict[str, Any]], energy_key: str) -> list[str]:
    if not records:
        return ["No records available."]
    lines = [
        "| rank | structure_id | site | orientation | height_angstrom | energy_ev | ks_status |",
        "| --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for rank, record in enumerate(records):
        energy = record.get(energy_key)
        energy_text = "" if energy is None else f"{float(energy):.8f}"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(rank),
                    str(record.get("structure_id", "")),
                    str(record.get("site", "")),
                    str(record.get("orientation", "")),
                    str(record.get("height_angstrom", "")),
                    energy_text,
                    str(record.get("ks_status", "")),
                ]
            )
            + " |"
        )
    return lines


def _read_excerpt(path: str | Path, max_lines: int = 12) -> str:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[:max_lines])


def _recommend(counts: dict[str, int | float | str | None]) -> list[str]:
    recommendations: list[str] = []
    parsed_converged = int(counts.get("parsed_converged") or 0)
    output_missing = int(counts.get("output_missing") or 0)
    selected_records = int(counts.get("selected_records") or 0)
    candidate_structures = int(counts.get("candidate_structures") or 0)
    corrected_records = int(counts.get("corrected_energy_records") or 0)

    if candidate_structures and candidate_structures < 100:
        recommendations.append("Increase candidate diversity if this is intended as a production adsorption search.")
    if selected_records and output_missing:
        recommendations.append("Run or attach QE outputs for missing selected jobs; KS labels are the current bottleneck.")
    if parsed_converged < 5:
        recommendations.append("Collect at least 5 parsed_converged KS labels before interpreting the delta model.")
    if parsed_converged >= 5 and corrected_records:
        recommendations.append("Use corrected_total_energy_ev for the next active-learning selection round.")
    if not recommendations:
        recommendations.append("Workflow state is healthy; proceed to the next active-learning round.")
    return recommendations
