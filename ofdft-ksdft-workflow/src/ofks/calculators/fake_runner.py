from __future__ import annotations

import time
from typing import Any

import numpy as np
from ase import Atoms

from ofks.calculators.base import CalculationResult


class FakeCalculatorRunner:
    """Deterministic toy calculator for workflow tests.

    The model is deliberately simple: it uses metadata from generated
    candidates to produce stable scores, then adds a tiny composition term
    so different systems do not collapse to identical energies.
    """

    backend = "fake"

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.site_offsets = config.get("site_offsets_ev", {})
        self.orientation_offsets = config.get("orientation_offsets_ev", {})
        height_model = config.get("height_model", {})
        self.optimum_height = float(height_model.get("optimum_angstrom", 2.5))
        self.stiffness = float(height_model.get("stiffness_ev_per_ang2", 0.2))
        force_model = config.get("force_model", {})
        self.force_scale = float(force_model.get("max_force_scale_ev_per_ang", 0.1))

    def calculate(self, atoms: Atoms) -> CalculationResult:
        started = time.perf_counter()
        height = float(atoms.info.get("height_angstrom", self.optimum_height))
        site = str(atoms.info.get("site", "default"))
        orientation = str(atoms.info.get("orientation", "default"))
        composition_term = _composition_term(atoms)
        height_penalty = self.stiffness * (height - self.optimum_height) ** 2
        site_offset = float(self.site_offsets.get(site, 0.05))
        orientation_offset = float(self.orientation_offsets.get(orientation, 0.0))
        lateral_term = _lateral_spread_term(atoms)
        total_energy = composition_term + height_penalty + site_offset + orientation_offset + lateral_term
        forces = self._fake_forces(atoms, height)
        runtime = time.perf_counter() - started
        return CalculationResult(
            backend=self.backend,
            total_energy_ev=float(total_energy),
            forces_ev_per_ang=forces,
            converged=True,
            runtime_seconds=runtime,
            metadata={
                "site_offset_ev": site_offset,
                "orientation_offset_ev": orientation_offset,
                "height_penalty_ev": height_penalty,
                "composition_term_ev": composition_term,
            },
        )

    def _fake_forces(self, atoms: Atoms, height: float) -> np.ndarray:
        forces = np.zeros((len(atoms), 3), dtype=float)
        if len(atoms) == 0:
            return forces
        adsorbate_count = _adsorbate_count(atoms)
        if adsorbate_count == 0:
            return forces
        deviation = height - self.optimum_height
        forces[-adsorbate_count:, 2] = -2.0 * self.stiffness * deviation / max(adsorbate_count, 1)
        max_norm = np.max(np.linalg.norm(forces, axis=1))
        if max_norm > self.force_scale and max_norm > 0:
            forces *= self.force_scale / max_norm
        return forces


def _composition_term(atoms: Atoms) -> float:
    numbers = atoms.get_atomic_numbers()
    return -0.001 * float(np.sum(numbers))


def _lateral_spread_term(atoms: Atoms) -> float:
    if len(atoms) < 2:
        return 0.0
    xy = atoms.positions[:, :2]
    spread = np.std(xy, axis=0)
    return 0.0001 * float(np.sum(spread))


def _adsorbate_count(atoms: Atoms) -> int:
    adsorbate = str(atoms.info.get("adsorbate", ""))
    if adsorbate.upper() == "H2O":
        return 3
    if adsorbate:
        return 1
    return 0
