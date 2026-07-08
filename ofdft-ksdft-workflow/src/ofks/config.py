from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class SurfaceConfig(BaseModel):
    element: str
    miller: list[int]
    size: tuple[int, int, int]
    vacuum_angstrom: float = 18.0
    fixed_layers: int = 0


class AdsorbateConfig(BaseModel):
    name: str
    orientations: list[str] = Field(default_factory=list)
    heights_angstrom: list[float] = Field(default_factory=lambda: [2.5])


class PlacementConfig(BaseModel):
    sites: list[str] = Field(default_factory=lambda: ["top"])
    lateral_jitter_angstrom: float = 0.0


class DeduplicationConfig(BaseModel):
    distance_tolerance_angstrom: float = 0.15


class SystemConfig(BaseModel):
    name: str
    surface: SurfaceConfig
    adsorbate: AdsorbateConfig
    placement: PlacementConfig = Field(default_factory=PlacementConfig)
    deduplication: DeduplicationConfig = Field(default_factory=DeduplicationConfig)
    references: dict[str, Any] = Field(default_factory=dict)


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in config file: {path}")
    return data


def load_system_config(path: str | Path) -> SystemConfig:
    return SystemConfig.model_validate(load_yaml(path))
