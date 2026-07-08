from __future__ import annotations

import hashlib
import re
from typing import Any

import numpy as np
from ase import Atoms

_STRUCTURE_ID_RE = re.compile(r"^[0-9a-f]{16}$")


def structure_hash(atoms: Atoms, decimals: int = 5) -> str:
    symbols = ",".join(atoms.get_chemical_symbols())
    positions = np.round(atoms.positions, decimals=decimals)
    cell = np.round(atoms.cell.array, decimals=decimals)
    payload = "|".join(
        [
            symbols,
            np.array2string(positions, separator=",", max_line_width=1_000_000),
            np.array2string(cell, separator=",", max_line_width=1_000_000),
            str(tuple(bool(x) for x in atoms.pbc)),
        ]
    )
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


def is_valid_structure_id(value: Any) -> bool:
    return isinstance(value, str) and _STRUCTURE_ID_RE.fullmatch(value) is not None


def get_structure_id(atoms: Atoms) -> str:
    existing = atoms.info.get("structure_id")
    if is_valid_structure_id(existing):
        return str(existing)
    structure_id = structure_hash(atoms)
    atoms.info["structure_id"] = structure_id
    return structure_id
