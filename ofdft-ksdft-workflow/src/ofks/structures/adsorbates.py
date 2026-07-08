from __future__ import annotations

from ase import Atoms
from ase.build import molecule


def build_adsorbate(name: str) -> Atoms:
    normalized = name.strip()
    upper = normalized.upper()
    if upper in {"H", "O", "C", "N"}:
        adsorbate = Atoms(upper, positions=[(0.0, 0.0, 0.0)])
    else:
        adsorbate = molecule(normalized)
    adsorbate.info["adsorbate_name"] = normalized
    return adsorbate


def orient_adsorbate(adsorbate: Atoms, orientation: str) -> Atoms:
    oriented = adsorbate.copy()
    orientation = orientation.lower()
    if len(oriented) == 1 or orientation == "atom":
        oriented.info["orientation"] = orientation
        return oriented

    if oriented.info.get("adsorbate_name", "").upper() == "H2O":
        # ASE H2O has O near the origin and a molecular plane in xz.
        if orientation == "dipole_up":
            pass
        elif orientation == "dipole_down":
            oriented.rotate(180, "x", center=(0, 0, 0))
        elif orientation == "flat":
            oriented.rotate(90, "y", center=(0, 0, 0))
        else:
            raise ValueError(f"Unsupported H2O orientation: {orientation}")
    elif orientation not in {"default", "upright", "flat"}:
        raise ValueError(f"Unsupported orientation for {oriented.info.get('adsorbate_name')}: {orientation}")

    oriented.info["orientation"] = orientation
    return oriented
