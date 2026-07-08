from __future__ import annotations

from ase import Atoms
from ase.build import fcc111, fcc100, hcp0001, surface
from ase.constraints import FixAtoms


def build_slab(
    element: str,
    miller: list[int] | tuple[int, ...],
    size: tuple[int, int, int],
    vacuum: float,
    fixed_layers: int = 0,
) -> Atoms:
    """Build a simple metal slab with optional bottom-layer constraints."""
    miller_tuple = tuple(miller)
    if element == "Al" and miller_tuple == (1, 1, 1):
        slab = fcc111(element, size=size, vacuum=vacuum, periodic=True)
    elif element == "Al" and miller_tuple == (1, 0, 0):
        slab = fcc100(element, size=size, vacuum=vacuum, periodic=True)
    elif element == "Mg" and miller_tuple in {(0, 0, 0, 1), (0, 0, 1)}:
        slab = hcp0001(element, size=size, vacuum=vacuum, periodic=True)
    else:
        if len(miller_tuple) == 4:
            raise ValueError("Generic ASE surface builder expects 3-index Miller notation")
        bulk_symbol = element
        slab = surface(bulk_symbol, miller_tuple, layers=size[2], vacuum=vacuum)
        slab = slab.repeat((size[0], size[1], 1))

    slab.info["surface_element"] = element
    slab.info["miller"] = list(miller_tuple)
    slab.info["slab_size"] = list(size)
    slab.info["vacuum_angstrom"] = float(vacuum)
    slab.info["fixed_layers"] = int(fixed_layers)

    if fixed_layers > 0:
        add_bottom_layer_constraint(slab, fixed_layers)
    return slab


def add_bottom_layer_constraint(slab: Atoms, fixed_layers: int) -> None:
    z_values = slab.positions[:, 2]
    unique_layers = sorted({round(float(z), 6) for z in z_values})
    if fixed_layers > len(unique_layers):
        raise ValueError("fixed_layers cannot exceed total slab layers")
    z_cut = unique_layers[fixed_layers - 1]
    fixed_indices = [atom.index for atom in slab if atom.position[2] <= z_cut + 1e-6]
    slab.set_constraint(FixAtoms(indices=fixed_indices))
    slab.info["fixed_atom_indices"] = fixed_indices
