from __future__ import annotations


def adsorption_energy(slab_adsorbate_ev: float, slab_ev: float, adsorbate_ev: float) -> float:
    return slab_adsorbate_ev - slab_ev - adsorbate_ev
