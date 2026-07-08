from __future__ import annotations

from itertools import product

import numpy as np
from ase import Atoms
from ase.build import add_adsorbate
from ase.geometry import get_distances

from ofks.config import SystemConfig
from ofks.structures.adsorbates import build_adsorbate, orient_adsorbate
from ofks.structures.slabs import build_slab
from ofks.utils.hashing import structure_hash


def enumerate_sites(slab: Atoms, site_types: list[str]) -> list[dict[str, object]]:
    top_positions = _top_layer_xy(slab)
    cell = slab.cell.array
    sites: list[dict[str, object]] = []

    if "top" in site_types:
        sites.extend({"site": "top", "xy": tuple(xy)} for xy in top_positions)

    if "bridge" in site_types and len(top_positions) >= 2:
        for xy_a, xy_b in _nearest_pairs(top_positions, cell):
            sites.append({"site": "bridge", "xy": tuple((xy_a + xy_b) / 2.0)})

    if any(site in site_types for site in ("fcc", "hcp")) and len(top_positions) >= 3:
        centers = _triangle_centers(top_positions)
        for index, center in enumerate(centers):
            site_name = "fcc" if index % 2 == 0 else "hcp"
            if site_name in site_types:
                sites.append({"site": site_name, "xy": tuple(center)})

    return _deduplicate_sites(sites)


def generate_adsorption_candidates(config: SystemConfig) -> list[Atoms]:
    slab = build_slab(
        element=config.surface.element,
        miller=config.surface.miller,
        size=config.surface.size,
        vacuum=config.surface.vacuum_angstrom,
        fixed_layers=config.surface.fixed_layers,
    )
    adsorbate = build_adsorbate(config.adsorbate.name)
    sites = enumerate_sites(slab, config.placement.sites)

    candidates: list[Atoms] = []
    for site, orientation, height in product(
        sites,
        config.adsorbate.orientations or ["default"],
        config.adsorbate.heights_angstrom,
    ):
        for jitter_index, jitter in enumerate(_jitter_offsets(config.placement.lateral_jitter_angstrom)):
            oriented = orient_adsorbate(adsorbate, orientation)
            candidate = slab.copy()
            xy = np.asarray(site["xy"], dtype=float) + jitter
            add_adsorbate(candidate, oriented, height=height, position=tuple(xy))
            candidate.info.update(
                {
                    "system_name": config.name,
                    "adsorbate": config.adsorbate.name,
                    "site": site["site"],
                    "orientation": orientation,
                    "height_angstrom": float(height),
                    "lateral_jitter_index": jitter_index,
                    "lateral_jitter_dx_angstrom": float(jitter[0]),
                    "lateral_jitter_dy_angstrom": float(jitter[1]),
                }
            )
            candidate.info["structure_id"] = structure_hash(candidate)
            candidates.append(candidate)

    if config.placement.lateral_jitter_angstrom > 0:
        return _deduplicate_by_structure_id(candidates)
    return deduplicate_structures(candidates, tolerance=config.deduplication.distance_tolerance_angstrom)


def deduplicate_structures(structures: list[Atoms], tolerance: float) -> list[Atoms]:
    unique: list[Atoms] = []
    fingerprints: list[np.ndarray] = []
    for atoms in structures:
        fp = _distance_fingerprint(atoms)
        if not any(np.allclose(fp, seen, atol=tolerance) for seen in fingerprints):
            unique.append(atoms)
            fingerprints.append(fp)
    return unique


def _deduplicate_by_structure_id(structures: list[Atoms]) -> list[Atoms]:
    unique = []
    seen: set[str] = set()
    for atoms in structures:
        structure_id = str(atoms.info.get("structure_id") or structure_hash(atoms))
        if structure_id in seen:
            continue
        seen.add(structure_id)
        unique.append(atoms)
    return unique


def _top_layer_xy(slab: Atoms) -> np.ndarray:
    z_values = slab.positions[:, 2]
    z_top = np.max(z_values)
    top_indices = np.where(z_values >= z_top - 0.25)[0]
    return slab.positions[top_indices, :2]


def _nearest_pairs(points: np.ndarray, cell: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    if len(points) < 2:
        return []
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            delta = points[i] - points[j]
            dist = np.linalg.norm(delta)
            distances.append((dist, points[i], points[j]))
    distances.sort(key=lambda item: item[0])
    if not distances:
        return []
    nearest = distances[0][0]
    return [(a, b) for dist, a, b in distances if dist <= nearest * 1.05]


def _triangle_centers(points: np.ndarray) -> list[np.ndarray]:
    centers: list[np.ndarray] = []
    if len(points) < 3:
        return centers
    centroid = np.mean(points, axis=0)
    ordered = sorted(points, key=lambda p: np.linalg.norm(p - centroid))
    for i in range(0, min(len(ordered) - 2, 8)):
        centers.append(np.mean(ordered[i : i + 3], axis=0))
    return centers


def _deduplicate_sites(sites: list[dict[str, object]], decimals: int = 6) -> list[dict[str, object]]:
    seen: set[tuple[str, float, float]] = set()
    unique: list[dict[str, object]] = []
    for site in sites:
        xy = site["xy"]
        assert isinstance(xy, tuple)
        key = (str(site["site"]), round(float(xy[0]), decimals), round(float(xy[1]), decimals))
        if key not in seen:
            seen.add(key)
            unique.append(site)
    return unique


def _jitter_offsets(radius: float) -> list[np.ndarray]:
    if radius <= 0:
        return [np.zeros(2, dtype=float)]
    value = float(radius)
    return [
        np.asarray([0.0, 0.0], dtype=float),
        np.asarray([value, 0.0], dtype=float),
        np.asarray([-value, 0.0], dtype=float),
        np.asarray([0.0, value], dtype=float),
        np.asarray([0.0, -value], dtype=float),
    ]


def _distance_fingerprint(atoms: Atoms) -> np.ndarray:
    _, distances = get_distances(atoms.positions, cell=atoms.cell, pbc=atoms.pbc)
    return np.sort(distances.reshape(-1))
