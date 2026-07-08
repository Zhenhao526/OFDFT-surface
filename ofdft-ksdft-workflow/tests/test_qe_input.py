from ase.constraints import FixAtoms

from ofks.calculators.qe_input import render_qe_input
from ofks.structures.slabs import build_slab


def test_qe_input_contains_required_cards_and_constraints():
    atoms = build_slab("Al", [1, 1, 1], size=(1, 1, 2), vacuum=8.0, fixed_layers=1)
    atoms.info["structure_id"] = "test"
    assert isinstance(atoms.constraints[0], FixAtoms)
    config = {
        "backend": "qe",
        "xc": "PBE",
        "pseudopotentials": {"Al": "Al.UPF"},
        "pseudo_dir": "/tmp/pseudo",
        "ecutwfc_ry": 40,
        "ecutrho_ry": 320,
        "kpoints": [2, 2, 1],
        "smearing": {"type": "cold", "degauss_ry": 0.02},
        "dipole_correction": True,
    }

    text = render_qe_input(atoms, config, prefix="test_prefix")

    assert "&CONTROL" in text
    assert "calculation = 'relax'" in text
    assert "ATOMIC_SPECIES" in text
    assert "Al.UPF" in text
    assert "pseudo_dir = '/tmp/pseudo'" in text
    assert "CELL_PARAMETERS angstrom" in text
    assert "ATOMIC_POSITIONS angstrom" in text
    assert "K_POINTS automatic" in text
    assert "2 2 1 0 0 0" in text
    assert "0 0 0" in text
    assert "1 1 1" in text


def test_qe_input_supports_scf_smoke_settings():
    atoms = build_slab("Mg", [0, 0, 0, 1], size=(1, 1, 2), vacuum=6.0, fixed_layers=1)
    config = {
        "backend": "qe",
        "calculation": "scf",
        "xc": "PBE",
        "pseudopotentials": {"Mg": "Mg.UPF"},
        "ecutwfc_ry": 25,
        "ecutrho_ry": 200,
        "kpoints": [1, 1, 1],
        "electrons": {"conv_thr": "1.0d-4", "mixing_beta": 0.4},
        "control": {"nstep": 20},
    }

    text = render_qe_input(atoms, config, prefix="smoke")

    assert "calculation = 'scf'" in text
    assert "nstep = 20" in text
    assert "conv_thr = 1.0d-4" in text
    assert "mixing_beta = 0.4" in text
    assert "&IONS" not in text
