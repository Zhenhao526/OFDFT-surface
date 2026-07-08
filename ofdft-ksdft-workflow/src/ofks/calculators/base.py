from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

import numpy as np
from ase import Atoms


@dataclass(frozen=True)
class CalculationResult:
    backend: str
    total_energy_ev: float
    forces_ev_per_ang: np.ndarray | None = None
    converged: bool = True
    runtime_seconds: float | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def max_force_ev_per_ang(self) -> float | None:
        if self.forces_ev_per_ang is None or self.forces_ev_per_ang.size == 0:
            return None
        norms = np.linalg.norm(self.forces_ev_per_ang, axis=1)
        return float(np.max(norms))


class CalculatorRunner(Protocol):
    backend: str

    def calculate(self, atoms: Atoms) -> CalculationResult:
        """Calculate a single structure and return a normalized result."""
