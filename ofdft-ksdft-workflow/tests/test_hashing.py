from ase import Atoms

from ofks.utils.hashing import get_structure_id, is_valid_structure_id


def test_get_structure_id_recomputes_invalid_extxyz_parsed_id():
    atoms = Atoms("MgO", positions=[(0, 0, 0), (0, 0, 2)])
    atoms.info["structure_id"] = float("inf")

    structure_id = get_structure_id(atoms)

    assert is_valid_structure_id(structure_id)
    assert atoms.info["structure_id"] == structure_id
