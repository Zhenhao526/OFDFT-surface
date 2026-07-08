from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

RY_TO_EV = 13.605693122994
BOHR_TO_ANGSTROM = 0.529177210903
RY_PER_BOHR_TO_EV_PER_ANG = RY_TO_EV / BOHR_TO_ANGSTROM

_TOTAL_ENERGY_RE = re.compile(r"!\s+total energy\s+=\s+([-+0-9.Ee]+)\s+Ry")
_FORCE_RE = re.compile(
    r"atom\s+\d+\s+type\s+\d+\s+force\s+=\s+"
    r"([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)"
)


@dataclass(frozen=True)
class QEParseResult:
    total_energy_ev: float | None
    forces_ev_per_ang: np.ndarray | None
    converged: bool
    job_done: bool
    raw_total_energy_ry: float | None

    @property
    def max_force_ev_per_ang(self) -> float | None:
        if self.forces_ev_per_ang is None or self.forces_ev_per_ang.size == 0:
            return None
        norms = np.linalg.norm(self.forces_ev_per_ang, axis=1)
        return float(np.max(norms))


def parse_qe_output(path: str | Path) -> QEParseResult:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    total_energy_ry = _parse_last_total_energy_ry(text)
    forces = _parse_last_force_block(text)
    job_done = "JOB DONE" in text
    converged = job_done and (
        "convergence has been achieved" in text
        or "End of BFGS Geometry Optimization" in text
        or "bfgs converged" in text.lower()
    )
    return QEParseResult(
        total_energy_ev=None if total_energy_ry is None else total_energy_ry * RY_TO_EV,
        forces_ev_per_ang=forces,
        converged=converged,
        job_done=job_done,
        raw_total_energy_ry=total_energy_ry,
    )


def _parse_last_total_energy_ry(text: str) -> float | None:
    matches = _TOTAL_ENERGY_RE.findall(text)
    if not matches:
        return None
    return float(matches[-1])


def _parse_last_force_block(text: str) -> np.ndarray | None:
    current: list[list[float]] = []
    blocks: list[list[list[float]]] = []
    in_force_block = False
    for line in text.splitlines():
        if "Forces acting on atoms" in line:
            if current:
                blocks.append(current)
            current = []
            in_force_block = True
            continue
        if not in_force_block:
            continue
        match = _FORCE_RE.search(line)
        if match:
            current.append([float(match.group(1)), float(match.group(2)), float(match.group(3))])
            continue
        if current and line.strip() == "":
            blocks.append(current)
            current = []
            in_force_block = False
    if current:
        blocks.append(current)
    if not blocks:
        return None
    return np.asarray(blocks[-1], dtype=float) * RY_PER_BOHR_TO_EV_PER_ANG
