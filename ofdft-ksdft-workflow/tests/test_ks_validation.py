from ase.io import read

from ofks.config import load_system_config, load_yaml
from ofks.structures.placements import generate_adsorption_candidates
from ofks.workflows.run_ks_validation import prepare_ks_validation_batch


def test_prepare_ks_validation_batch_writes_qe_inputs(tmp_path):
    system_config = load_system_config("configs/systems/mg0001_o.yaml")
    atoms_list = generate_adsorption_candidates(system_config)[:2]
    selected = [
        {
            "structure_id": atoms_list[0].info["structure_id"],
            "system_name": "mg0001_o",
            "selection_rank": 0,
            "site": atoms_list[0].info["site"],
            "orientation": atoms_list[0].info["orientation"],
        }
    ]
    calculator_config = load_yaml("configs/calculators/qe_pbe.yaml")

    records = prepare_ks_validation_batch(selected, atoms_list, calculator_config, tmp_path)

    assert len(records) == 1
    assert records[0]["ks_status"] == "input_prepared"
    input_text = (tmp_path / f"0000_{atoms_list[0].info['structure_id']}" / "pw.in").read_text()
    assert "Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF" in input_text
    assert "O.pbe-n-kjpaw_psl.1.0.0.UPF" in input_text
    reloaded = read(records[0]["ks_structure"])
    assert len(reloaded) == len(atoms_list[0])
