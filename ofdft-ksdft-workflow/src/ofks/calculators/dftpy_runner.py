from __future__ import annotations

import contextlib
import io
import re
import time
from pathlib import Path
from typing import Any

import numpy as np
from ase import Atoms

from ofks.calculators.base import CalculationResult


class DftpyCalculatorRunner:
    """DFTpy-backed OFDFT single-point runner.

    DFTpy is kept as an optional dependency. Imports happen inside
    ``calculate`` and config construction so the rest of the workflow can run
    without DFTpy installed.
    """

    backend = "dftpy"

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.pseudo_dir = Path(str(config.get("pseudo_dir", "pseudo")))
        self.pseudopotentials = _pseudopotential_map(config)
        self.kedf = str(config.get("kedf", "WT"))
        self.xc = str(config.get("xc", "LDA"))
        self.grid_spacing = config.get("grid_spacing_angstrom")
        self.grid_ecut = config.get("grid_ecut_ev")
        self.quiet = bool(config.get("quiet", True))

    def calculate(self, atoms: Atoms) -> CalculationResult:
        started = time.perf_counter()
        _validate_pseudopotentials(atoms, self.pseudopotentials, self.pseudo_dir)
        dftpy_config = build_dftpy_config(self.config, atoms=atoms)
        work_atoms = atoms.copy()
        log_text = ""

        def _run() -> tuple[float, np.ndarray]:
            from dftpy.api.api4ase import DFTpyCalculator

            work_atoms.calc = DFTpyCalculator(config=dftpy_config, zero_stress=True)
            energy = float(work_atoms.get_potential_energy())
            forces = np.asarray(work_atoms.get_forces(), dtype=float)
            return energy, forces

        try:
            if self.quiet:
                stdout_buffer = io.StringIO()
                stderr_buffer = io.StringIO()
                with _redirect_dftpy_stdout(stdout_buffer):
                    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                        energy, forces = _run()
                log_text = stdout_buffer.getvalue() + stderr_buffer.getvalue()
            else:
                stdout_buffer = io.StringIO()
                with _redirect_dftpy_stdout(stdout_buffer):
                    energy, forces = _run()
                log_text = stdout_buffer.getvalue()
        except ModuleNotFoundError as exc:
            raise RuntimeError(_dependency_error_message(exc, self.xc)) from exc

        runtime = time.perf_counter() - started
        log_summary = parse_dftpy_log(log_text)
        converged = bool(log_summary["density_converged"])
        return CalculationResult(
            backend=self.backend,
            total_energy_ev=energy,
            forces_ev_per_ang=forces,
            converged=converged,
            runtime_seconds=runtime,
            metadata={
                "kedf": self.kedf,
                "xc": self.xc,
                "grid_spacing_angstrom": self.grid_spacing,
                "grid_ecut_ev": self.grid_ecut,
                "density_converged": converged,
                "density_iterations": log_summary["density_iterations"],
                "density_reached_max_steps": log_summary["density_reached_max_steps"],
                "optimization": dict(self.config.get("optimization", {})),
                "log_excerpt": _log_excerpt(log_text),
                "pseudopotentials": dict(self.pseudopotentials),
                "pseudo_dir": str(self.pseudo_dir),
            },
        )


def build_dftpy_config(config: dict[str, Any], atoms: Atoms | None = None) -> dict[str, Any]:
    from dftpy.config.config import DefaultOption

    dftpy_config = DefaultOption()
    pseudo_dir = Path(str(config.get("pseudo_dir", "pseudo")))
    dftpy_config["PATH"]["pppath"] = str(pseudo_dir.resolve())
    dftpy_config["PP"].update(_pseudopotential_map(config))

    spacing = config.get("grid_spacing_angstrom")
    if spacing is not None:
        dftpy_config["GRID"]["spacing"] = float(spacing)
    ecut = config.get("grid_ecut_ev")
    if ecut is not None:
        dftpy_config["GRID"]["ecut"] = float(ecut)

    dftpy_config["EXC"]["xc"] = str(config.get("xc", "LDA"))
    dftpy_config["KEDF"]["kedf"] = str(config.get("kedf", "WT"))
    kedf_options = config.get("kedf_options", {})
    if kedf_options:
        if not isinstance(kedf_options, dict):
            raise ValueError("DFTpy calculator config field 'kedf_options' must be a mapping.")
        dftpy_config["KEDF"].update(kedf_options)
    dftpy_config["DENSITY"]["densityini"] = str(config.get("density_initial", "heg"))
    dftpy_config["MATH"]["reuse"] = bool(config.get("reuse_density", False))

    optimization = config.get("optimization", {})
    if "method" in optimization:
        dftpy_config["OPT"]["method"] = str(optimization["method"])
    if "algorithm" in optimization:
        dftpy_config["OPT"]["algorithm"] = str(optimization["algorithm"])
    if "maxiter" in optimization:
        dftpy_config["OPT"]["maxiter"] = int(optimization["maxiter"])
    if "maxfun" in optimization:
        dftpy_config["OPT"]["maxfun"] = int(optimization["maxfun"])
    if "econv" in optimization:
        dftpy_config["OPT"]["econv"] = float(optimization["econv"])

    if atoms is not None:
        _validate_pseudopotentials(atoms, dftpy_config["PP"], pseudo_dir)
    return dftpy_config


def _pseudopotential_map(config: dict[str, Any]) -> dict[str, str]:
    if "pseudopotentials" in config:
        return {str(key).capitalize(): str(value) for key, value in config["pseudopotentials"].items()}
    element = config.get("element")
    pseudopotential = config.get("pseudopotential")
    if element and pseudopotential:
        return {str(element).capitalize(): str(pseudopotential)}
    raise ValueError("DFTpy calculator config requires 'pseudopotentials' or 'element' plus 'pseudopotential'.")


def _validate_pseudopotentials(atoms: Atoms, pseudopotentials: dict[str, str], pseudo_dir: Path) -> None:
    missing_species = sorted(set(atoms.get_chemical_symbols()) - set(pseudopotentials))
    if missing_species:
        raise ValueError(f"Missing DFTpy pseudopotentials for species: {', '.join(missing_species)}")
    missing_files = [
        str(pseudo_dir / filename)
        for filename in pseudopotentials.values()
        if not (pseudo_dir / filename).exists()
    ]
    if missing_files:
        raise FileNotFoundError("Missing DFTpy pseudopotential files: " + ", ".join(missing_files))


@contextlib.contextmanager
def _redirect_dftpy_stdout(buffer: io.StringIO):
    try:
        from dftpy.constants import environ
    except Exception:
        yield
        return

    previous = environ.get("STDOUT")
    environ["STDOUT"] = buffer
    try:
        yield
    finally:
        if previous is None:
            environ.pop("STDOUT", None)
        else:
            environ["STDOUT"] = previous


def _dependency_error_message(exc: ModuleNotFoundError, xc: str) -> str:
    name = str(exc.name or "")
    if name == "dftpy":
        return "DFTpy is not installed. Install the optional OFDFT dependencies before using backend: dftpy."
    if name.startswith("pylibxc"):
        return (
            f"DFTpy XC={xc!r} requires pylibxc.functional, which is not available in this environment. "
            "Use xc: LDA without an incomplete pylibxc namespace for a local smoke run, "
            "or install a working LibXC/pylibxc binding for PBE."
        )
    return str(exc)


def parse_dftpy_log(text: str) -> dict[str, object]:
    step_numbers = []
    for line in text.splitlines():
        match = re.match(r"^\s*(\d+)\s+[-+0-9.Ee]+", line)
        if match:
            step_numbers.append(int(match.group(1)))
    reached_max_steps = "Not converged" in text or "reached max steps" in text
    return {
        "density_converged": not reached_max_steps,
        "density_reached_max_steps": reached_max_steps,
        "density_iterations": (max(step_numbers) + 1) if step_numbers else None,
    }


def _log_excerpt(text: str, max_lines: int = 16) -> str:
    if not text:
        return ""
    lines = [line for line in text.splitlines() if line.strip()]
    warning_lines = [line for line in lines if "WARN" in line or "Not converged" in line]
    tail_lines = lines[-max_lines:]
    selected = []
    for line in warning_lines + tail_lines:
        if line not in selected:
            selected.append(line)
    return "\n".join(selected[-max_lines:])
