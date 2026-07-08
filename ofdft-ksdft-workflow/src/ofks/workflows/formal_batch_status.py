from __future__ import annotations

import json
from pathlib import Path
from statistics import median
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl

app = typer.Typer(help="Summarize formal OFDFT/KSDFT benchmark batch progress.")
console = Console()


@app.command()
def main(
    system: str = typer.Option(..., "--system"),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    structures: Path | None = typer.Option(None, "--structures", exists=True, file_okay=True, dir_okay=False),
    selected: Path | None = typer.Option(None, "--selected", exists=True, file_okay=True, dir_okay=False),
    ks_labels: Path | None = typer.Option(None, "--ks-labels", exists=True, file_okay=True, dir_okay=False),
    missing: Path | None = typer.Option(None, "--missing", exists=True, file_okay=True, dir_okay=False),
    candidate_output: list[str] = typer.Option(
        [],
        "--candidate-output",
        help="Candidate output as NAME=PATH. Can be repeated.",
    ),
    benchmark: list[Path] = typer.Option(
        [],
        "--benchmark",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Benchmark JSON report. Can be repeated.",
    ),
) -> None:
    report = build_status_report(
        system=system,
        structures=structures,
        selected=selected,
        ks_labels=ks_labels,
        missing=missing,
        candidate_outputs=_parse_named_paths(candidate_output),
        benchmarks=benchmark,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    console.print(f"Wrote formal batch status report to {out}")


def build_status_report(
    system: str,
    structures: Path | None = None,
    selected: Path | None = None,
    ks_labels: Path | None = None,
    missing: Path | None = None,
    candidate_outputs: dict[str, Path] | None = None,
    benchmarks: list[Path] | None = None,
) -> str:
    candidate_outputs = candidate_outputs or {}
    benchmarks = benchmarks or []
    lines = [
        f"# Formal Batch Status: {system}",
        "",
        "## Inputs",
        "",
        "| artifact | path | records | status |",
        "| --- | --- | ---: | --- |",
    ]

    structure_count = _count_structures(structures) if structures is not None else None
    selected_records = _read_optional_jsonl(selected)
    ks_records = _read_optional_jsonl(ks_labels)
    missing_records = _read_optional_jsonl(missing)

    lines.append(_input_row("structures", structures, structure_count, "present" if structures else "not provided"))
    lines.append(_input_row("selected KS batch", selected, _len_or_none(selected_records), _status_from_records(selected_records)))
    lines.append(_input_row("KS labels", ks_labels, _len_or_none(ks_records), _ks_completion_text(ks_records)))
    lines.append(_input_row("missing KS jobs", missing, _len_or_none(missing_records), _missing_text(missing_records)))

    lines.extend(["", "## KSDFT Completion", ""])
    if ks_records is None:
        lines.append("- KS labels not provided.")
    else:
        counts = _count_by_key(ks_records, "ks_status")
        parsed = counts.get("parsed_converged", 0)
        total = len(ks_records)
        lines.append(f"- Parsed converged: {parsed}/{total} ({_percent(parsed, total)})")
        lines.append(f"- Status counts: `{json.dumps(counts, ensure_ascii=False, sort_keys=True)}`")
        runtimes = [_first_float(record, ("qe_runtime_seconds", "ks_runtime_seconds")) for record in ks_records]
        runtime_values = [value for value in runtimes if value is not None]
        if runtime_values:
            lines.append(
                f"- QE runtime: total {_fmt(sum(runtime_values))} s, median {_fmt(median(runtime_values))} s/structure"
            )

    lines.extend(["", "## Candidate Outputs", ""])
    if not candidate_outputs:
        lines.append("- No candidate outputs provided.")
    else:
        lines.extend(
            [
                "| candidate | path | records | converged | total runtime (s) | median runtime (s) |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for name, path in candidate_outputs.items():
            records = read_jsonl(path)
            converged = sum(1 for record in records if record.get("converged") is not False)
            runtimes = [_first_float(record, ("runtime_seconds",)) for record in records]
            runtime_values = [value for value in runtimes if value is not None]
            total_runtime = sum(runtime_values) if runtime_values else None
            median_runtime = median(runtime_values) if runtime_values else None
            lines.append(
                "| "
                + " | ".join(
                    [
                        name,
                        _path_text(path),
                        str(len(records)),
                        str(converged),
                        _fmt(total_runtime),
                        _fmt(median_runtime),
                    ]
                )
                + " |"
            )

    lines.extend(["", "## Benchmarks", ""])
    benchmark_rows = _benchmark_rows(benchmarks)
    if not benchmark_rows:
        lines.append("- No benchmark reports provided.")
    else:
        lines.extend(
            [
                "| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |",
                "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        lines.extend(benchmark_rows)

    lines.extend(["", "## Readiness", ""])
    lines.extend(_readiness_lines(structure_count, selected_records, ks_records, missing_records, candidate_outputs))
    lines.append("")
    return "\n".join(lines)


def _parse_named_paths(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise typer.BadParameter(f"Expected NAME=PATH, got: {value}")
        name, raw_path = value.split("=", 1)
        name = name.strip()
        if not name:
            raise typer.BadParameter(f"Candidate output name is empty in: {value}")
        path = Path(raw_path).expanduser()
        if not path.exists():
            raise typer.BadParameter(f"Candidate output path does not exist: {path}")
        parsed[name] = path
    return parsed


def _count_structures(path: Path | None) -> int | None:
    if path is None:
        return None
    from ase.io import read

    return len(read(path, ":"))


def _read_optional_jsonl(path: Path | None) -> list[dict[str, Any]] | None:
    if path is None:
        return None
    return read_jsonl(path)


def _input_row(name: str, path: Path | None, records: int | None, status: str) -> str:
    return f"| {name} | {_path_text(path)} | {_fmt(records)} | {status} |"


def _path_text(path: Path | None) -> str:
    return "" if path is None else str(path)


def _len_or_none(records: list[dict[str, Any]] | None) -> int | None:
    return None if records is None else len(records)


def _status_from_records(records: list[dict[str, Any]] | None) -> str:
    if records is None:
        return "not provided"
    return "empty" if not records else "present"


def _ks_completion_text(records: list[dict[str, Any]] | None) -> str:
    if records is None:
        return "not provided"
    if not records:
        return "empty"
    parsed = sum(1 for record in records if record.get("ks_status") == "parsed_converged")
    return f"{parsed}/{len(records)} parsed_converged"


def _missing_text(records: list[dict[str, Any]] | None) -> str:
    if records is None:
        return "not provided"
    if not records:
        return "none"
    return "needs QE run"


def _count_by_key(records: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(record.get(key, "missing"))
        counts[value] = counts.get(value, 0) + 1
    return counts


def _benchmark_rows(paths: list[Path]) -> list[str]:
    rows = []
    for path in paths:
        report = json.loads(path.read_text(encoding="utf-8"))
        for algo in report.get("algorithms", []):
            rows.append(
                "| "
                + " | ".join(
                    [
                        str(path),
                        str(algo.get("name", "")),
                        _fmt(algo.get("n_matched")),
                        _fmt(algo.get("energy_raw_mae_ev")),
                        _fmt(algo.get("adsorption_energy_raw_mae_ev")),
                        _fmt(algo.get("spearman_energy", algo.get("adsorption_spearman_energy"))),
                        _fmt(algo.get("speedup_vs_truth")),
                    ]
                )
                + " |"
            )
    return rows


def _readiness_lines(
    structure_count: int | None,
    selected_records: list[dict[str, Any]] | None,
    ks_records: list[dict[str, Any]] | None,
    missing_records: list[dict[str, Any]] | None,
    candidate_outputs: dict[str, Path],
) -> list[str]:
    lines = []
    if structure_count is None:
        lines.append("- Structure file was not provided; cannot verify formal pool size.")
    if selected_records is None or not selected_records:
        lines.append("- KS selection batch is missing or empty; run active selection before formal KSDFT.")
    if ks_records is None:
        lines.append("- KS labels are missing; pure KSDFT ground truth is not ready.")
    elif any(record.get("ks_status") != "parsed_converged" for record in ks_records):
        lines.append("- KS labels are incomplete; continue QE runs and re-parse outputs.")
    if missing_records:
        lines.append(f"- Missing QE jobs remain: {len(missing_records)}.")
    if not candidate_outputs:
        lines.append("- Candidate OFDFT outputs are missing; run DFTpy/OFDFT screening for the selected structures.")
    if not lines:
        lines.append("- Batch has KS labels and candidate outputs; ready for benchmark/delta training.")
    return lines


def _first_float(record: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        value = record.get(key)
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def _percent(part: int, total: int) -> str:
    if total == 0:
        return "n/a"
    return f"{part / total:.1%}"


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, int):
        return str(value)
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


if __name__ == "__main__":
    app()
