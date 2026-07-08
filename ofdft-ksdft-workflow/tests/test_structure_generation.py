from ofks.config import load_system_config
from ofks.config import SystemConfig
from ofks.structures.adsorbates import build_adsorbate
from ofks.structures.placements import enumerate_sites, generate_adsorption_candidates
from ofks.structures.slabs import build_slab


def test_build_al111_slab_has_expected_atom_count():
    slab = build_slab("Al", [1, 1, 1], size=(2, 2, 3), vacuum=12.0, fixed_layers=1)
    assert len(slab) == 12
    assert slab.pbc.all()
    assert slab.constraints


def test_build_mg0001_slab_has_expected_atom_count():
    slab = build_slab("Mg", [0, 0, 0, 1], size=(2, 2, 3), vacuum=12.0, fixed_layers=1)
    assert len(slab) == 12
    assert slab.constraints


def test_build_adsorbate_atom_and_water():
    assert len(build_adsorbate("O")) == 1
    assert len(build_adsorbate("H2O")) == 3


def test_enumerate_sites_returns_requested_types():
    slab = build_slab("Al", [1, 1, 1], size=(2, 2, 3), vacuum=12.0)
    sites = enumerate_sites(slab, ["top", "bridge", "fcc", "hcp"])
    site_names = {site["site"] for site in sites}
    assert {"top", "bridge"}.issubset(site_names)


def test_generate_candidates_from_config():
    config = load_system_config("configs/systems/al111_h2o.yaml")
    candidates = generate_adsorption_candidates(config)
    assert candidates
    assert all("structure_id" in atoms.info for atoms in candidates)


def test_generate_candidates_uses_lateral_jitter():
    base = load_system_config("configs/systems/mg0001_o_smoke.yaml")
    config = SystemConfig.model_validate(
        {
            **base.model_dump(),
            "placement": {
                **base.placement.model_dump(),
                "sites": ["top"],
                "lateral_jitter_angstrom": 0.2,
            },
            "adsorbate": {
                **base.adsorbate.model_dump(),
                "heights_angstrom": [2.0],
            },
        }
    )

    candidates = generate_adsorption_candidates(config)

    assert len(candidates) >= 5
    assert {atoms.info["lateral_jitter_index"] for atoms in candidates} >= {0, 1, 2, 3, 4}
    assert any(atoms.info["lateral_jitter_dx_angstrom"] != 0.0 for atoms in candidates)
