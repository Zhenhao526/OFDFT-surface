import pytest
from ase import Atoms

from ofks.calculators.dftpy_runner import DftpyCalculatorRunner, build_dftpy_config, parse_dftpy_log
from ofks.calculators.factory import build_calculator


def test_dftpy_factory_builds_runner(tmp_path):
    config = tmp_path / "dftpy.yaml"
    config.write_text(
        "\n".join(
            [
                "backend: dftpy",
                "xc: LDA",
                "kedf: WT",
                "pseudopotentials:",
                "  Mg: Mg.UPF",
            ]
        ),
        encoding="utf-8",
    )

    runner = build_calculator(config)

    assert isinstance(runner, DftpyCalculatorRunner)


def test_dftpy_config_builder_maps_project_yaml():
    pytest.importorskip("dftpy")
    atoms = Atoms("MgO", positions=[(0, 0, 0), (0, 0, 2)], cell=[8, 8, 8], pbc=True)
    config = {
        "backend": "dftpy",
        "xc": "LDA",
        "kedf": "WT",
        "kedf_options": {"lumpfactor": 0.25, "maxpoints": 200},
        "grid_spacing_angstrom": 0.8,
        "pseudo_dir": "pseudo",
        "pseudopotentials": {
            "Mg": "Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF",
            "O": "O.pbe-n-kjpaw_psl.1.0.0.UPF",
        },
        "optimization": {"maxiter": 3, "maxfun": 3, "econv": 1.0e-4},
    }

    dftpy_config = build_dftpy_config(config, atoms=atoms)

    assert dftpy_config["EXC"]["xc"] == "LDA"
    assert dftpy_config["KEDF"]["kedf"] == "WT"
    assert dftpy_config["KEDF"]["lumpfactor"] == 0.25
    assert dftpy_config["KEDF"]["maxpoints"] == 200
    assert dftpy_config["GRID"]["spacing"] == 0.8
    assert dftpy_config["PP"]["Mg"].endswith(".UPF")
    assert dftpy_config["PP"]["O"].endswith(".UPF")


def test_dftpy_runner_reports_missing_species():
    atoms = Atoms("MgO", positions=[(0, 0, 0), (0, 0, 2)], cell=[8, 8, 8], pbc=True)
    runner = DftpyCalculatorRunner(
        {
            "backend": "dftpy",
            "xc": "LDA",
            "kedf": "WT",
            "grid_spacing_angstrom": 0.8,
            "pseudo_dir": "pseudo",
            "pseudopotentials": {"Mg": "Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF"},
        }
    )

    with pytest.raises(ValueError, match="Missing DFTpy pseudopotentials"):
        runner.calculate(atoms)


def test_dftpy_runner_can_mark_nonconverged(monkeypatch):
    pytest.importorskip("dftpy")
    atoms = Atoms("Mg", positions=[(0, 0, 0)], cell=[8, 8, 8], pbc=True)
    runner = DftpyCalculatorRunner(
        {
            "backend": "dftpy",
            "xc": "LDA",
            "kedf": "WT",
            "grid_spacing_angstrom": 0.8,
            "pseudo_dir": "pseudo",
            "pseudopotentials": {"Mg": "Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF"},
            "optimization": {"maxiter": 1, "maxfun": 1, "econv": 1.0e-12},
        }
    )

    result = runner.calculate(atoms)

    assert result.converged is False
    assert result.metadata["density_converged"] is False
    assert "Not converged" in result.metadata["log_excerpt"]


def test_parse_dftpy_log_extracts_iterations():
    summary = parse_dftpy_log(
        "\n".join(
            [
                "Step    Energy(a.u.)",
                "0       -1.0",
                "1       -2.0",
                "!WARN: Not converged, but reached max steps",
            ]
        )
    )

    assert summary["density_converged"] is False
    assert summary["density_reached_max_steps"] is True
    assert summary["density_iterations"] == 2
