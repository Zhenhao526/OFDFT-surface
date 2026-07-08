from __future__ import annotations

import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class QEEnvironmentCheck:
    command: str
    command_path: str | None
    command_ok: bool
    pseudo_dir: str
    pseudo_dir_exists: bool
    missing_pseudopotentials: list[str]

    @property
    def ok(self) -> bool:
        return self.command_ok and self.pseudo_dir_exists and not self.missing_pseudopotentials


def check_qe_environment(
    calculator_config: dict[str, Any],
    pw_command: str = "pw.x",
    base_dir: str | Path = ".",
) -> QEEnvironmentCheck:
    command_path = resolve_command_path(pw_command)
    pseudo_dir = resolve_pseudo_dir(calculator_config, base_dir=base_dir)
    pseudo_map = calculator_config.get("pseudopotentials", {})
    missing = []
    for pseudo_name in pseudo_map.values():
        pseudo_path = pseudo_dir / str(pseudo_name)
        if not pseudo_path.exists():
            missing.append(str(pseudo_name))
    return QEEnvironmentCheck(
        command=pw_command,
        command_path=command_path,
        command_ok=command_path is not None,
        pseudo_dir=str(pseudo_dir),
        pseudo_dir_exists=pseudo_dir.exists(),
        missing_pseudopotentials=missing,
    )


def render_qe_environment_report(check: QEEnvironmentCheck) -> str:
    lines = [
        "# Quantum ESPRESSO Environment Check",
        "",
        f"- Command: `{check.command}`",
        f"- Command path: `{check.command_path}`" if check.command_path else "- Command path: missing",
        f"- Command OK: {check.command_ok}",
        f"- Pseudo dir: `{check.pseudo_dir}`",
        f"- Pseudo dir exists: {check.pseudo_dir_exists}",
        f"- Missing pseudopotentials: {len(check.missing_pseudopotentials)}",
    ]
    if check.missing_pseudopotentials:
        lines.append("")
        lines.append("## Missing Pseudopotentials")
        lines.extend(f"- {name}" for name in check.missing_pseudopotentials)
    lines.append("")
    lines.append("## Result")
    lines.append("OK" if check.ok else "Not ready")
    lines.append("")
    return "\n".join(lines)


def run_qe_jobs(
    records: list[dict[str, Any]],
    pw_command: str = "pw.x",
    output_name: str = "pw.out",
    input_name: str = "pw.in",
    limit: int | None = None,
    skip_existing: bool = True,
    timeout_seconds: int | None = None,
    pseudo_source: str | Path | None = None,
    job_pseudo_dir: str = "pseudo",
) -> list[dict[str, Any]]:
    selected = records[:limit] if limit is not None else records
    try:
        command_tokens = resolve_command_tokens(pw_command)
    except FileNotFoundError as exc:
        return [_run_status(record, "command_missing", error=str(exc), output_name=output_name) for record in selected]

    results = []
    for record in selected:
        results.append(
            run_qe_job(
                record,
                command_tokens=command_tokens,
                output_name=output_name,
                input_name=input_name,
                skip_existing=skip_existing,
                timeout_seconds=timeout_seconds,
                pseudo_source=pseudo_source,
                job_pseudo_dir=job_pseudo_dir,
            )
        )
    return results


def run_qe_job(
    record: dict[str, Any],
    command_tokens: list[str],
    output_name: str = "pw.out",
    input_name: str = "pw.in",
    skip_existing: bool = True,
    timeout_seconds: int | None = None,
    pseudo_source: str | Path | None = None,
    job_pseudo_dir: str = "pseudo",
) -> dict[str, Any]:
    job_dir = Path(str(record["ks_job_dir"]))
    input_path = job_dir / input_name
    output_path = job_dir / output_name
    if skip_existing and output_path.exists():
        return _run_status(record, "skipped_existing", output_path=output_path)
    if not input_path.exists():
        return _run_status(record, "input_missing", output_path=output_path, error=f"Missing {input_path}")
    if pseudo_source is not None:
        pseudo_ready = ensure_job_pseudo_link(job_dir, pseudo_source=Path(pseudo_source), link_name=job_pseudo_dir)
        if not pseudo_ready:
            return _run_status(
                record,
                "pseudo_source_missing",
                output_path=output_path,
                error=f"Missing pseudo source: {pseudo_source}",
            )

    started = time.perf_counter()
    with output_path.open("w", encoding="utf-8") as handle:
        try:
            completed = subprocess.run(
                [*command_tokens, "-in", input_name],
                cwd=job_dir,
                stdout=handle,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return _run_status(
                record,
                "timeout",
                output_path=output_path,
                runtime_seconds=time.perf_counter() - started,
                error=str(exc),
            )
    status = "exit_0" if completed.returncode == 0 else "exit_nonzero"
    return _run_status(
        record,
        status,
        output_path=output_path,
        runtime_seconds=time.perf_counter() - started,
        returncode=completed.returncode,
    )


def resolve_command_tokens(command: str) -> list[str]:
    tokens = shlex.split(command)
    if not tokens:
        raise FileNotFoundError("Empty QE command")
    first = tokens[0]
    resolved = resolve_command_path(first)
    if resolved is None:
        raise FileNotFoundError(f"Executable not found: {first}")
    return [resolved, *tokens[1:]]


def resolve_command_path(command: str) -> str | None:
    tokens = shlex.split(command)
    if not tokens:
        return None
    executable = tokens[0]
    if "/" in executable:
        path = Path(executable)
        return str(path.resolve()) if path.exists() else None
    return shutil.which(executable)


def resolve_pseudo_dir(calculator_config: dict[str, Any], base_dir: str | Path = ".") -> Path:
    pseudo_dir = Path(str(calculator_config.get("pseudo_dir", "./pseudo"))).expanduser()
    if not pseudo_dir.is_absolute():
        pseudo_dir = Path(base_dir) / pseudo_dir
    return pseudo_dir.resolve()


def ensure_job_pseudo_link(job_dir: str | Path, pseudo_source: str | Path, link_name: str = "pseudo") -> bool:
    source = Path(pseudo_source).expanduser()
    if not source.exists():
        return False
    link_path = Path(job_dir) / link_name
    if link_path.exists() or link_path.is_symlink():
        return True
    link_path.symlink_to(source.resolve(), target_is_directory=True)
    return True


def _run_status(
    record: dict[str, Any],
    status: str,
    output_path: str | Path | None = None,
    runtime_seconds: float | None = None,
    returncode: int | None = None,
    error: str | None = None,
    output_name: str = "pw.out",
) -> dict[str, Any]:
    job_dir = Path(str(record.get("ks_job_dir", ".")))
    output = Path(output_path) if output_path is not None else job_dir / output_name
    enriched = dict(record)
    enriched.update(
        {
            "qe_run_status": status,
            "ks_output": str(output),
            "qe_runtime_seconds": runtime_seconds,
            "qe_returncode": returncode,
        }
    )
    if error:
        enriched["qe_run_error"] = error
    return enriched
