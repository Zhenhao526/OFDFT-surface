from __future__ import annotations

from pydantic import BaseModel, Field


class CalculationRecord(BaseModel):
    backend: str
    converged: bool = False
    total_energy_ev: float | None = None
    adsorption_energy_ev: float | None = None
    max_force_ev_per_ang: float | None = None
    runtime_seconds: float | None = None


class StructureRecord(BaseModel):
    structure_id: str
    system_name: str
    surface: str
    adsorbate: str
    site: str
    orientation: str
    height_angstrom: float
    files: dict[str, str] = Field(default_factory=dict)
    calculation: CalculationRecord | None = None
