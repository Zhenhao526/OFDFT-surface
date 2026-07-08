from ase import Atoms

from ofks.calculators.fake_runner import FakeCalculatorRunner


def test_fake_calculator_is_deterministic():
    atoms = Atoms("Al4H", positions=[(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0.5, 0.5, 2.4)])
    atoms.info.update({"site": "fcc", "orientation": "atom", "height_angstrom": 2.4, "adsorbate": "H"})
    runner = FakeCalculatorRunner(
        {
            "backend": "fake",
            "site_offsets_ev": {"fcc": 0.0},
            "orientation_offsets_ev": {"atom": 0.0},
            "height_model": {"optimum_angstrom": 2.45, "stiffness_ev_per_ang2": 0.18},
        }
    )

    first = runner.calculate(atoms)
    second = runner.calculate(atoms)

    assert first.total_energy_ev == second.total_energy_ev
    assert first.forces_ev_per_ang is not None
    assert first.forces_ev_per_ang.shape == (len(atoms), 3)
