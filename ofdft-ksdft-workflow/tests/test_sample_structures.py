from ase import Atoms
import numpy as np

from ofks.workflows.sample_structures import _record, sample_structures


def _atoms(structure_id: str, site: str, jitter: int):
    atoms = Atoms("H", positions=[(float(jitter), 0.0, 0.0)])
    atoms.info["structure_id"] = structure_id
    atoms.info["site"] = site
    atoms.info["height_angstrom"] = 2.0
    atoms.info["lateral_jitter_index"] = jitter
    return atoms


def test_sample_structures_excludes_ids_and_round_robins_groups():
    atoms_list = [
        _atoms("aaaaaaaaaaaaaaaa", "top", 0),
        _atoms("bbbbbbbbbbbbbbbb", "top", 1),
        _atoms("cccccccccccccccc", "bridge", 0),
        _atoms("dddddddddddddddd", "bridge", 1),
    ]

    selected = sample_structures(
        atoms_list,
        max_count=3,
        excluded_ids={"aaaaaaaaaaaaaaaa"},
        group_keys=["site"],
    )

    assert [atoms.info["structure_id"] for atoms in selected] == [
        "cccccccccccccccc",
        "bbbbbbbbbbbbbbbb",
        "dddddddddddddddd",
    ]


def test_sample_structure_record_converts_numpy_scalars():
    atoms = _atoms("aaaaaaaaaaaaaaaa", "top", 0)
    atoms.info["lateral_jitter_index"] = np.int64(2)

    record = _record(0, atoms)

    assert record["lateral_jitter_index"] == 2
    assert isinstance(record["lateral_jitter_index"], int)
