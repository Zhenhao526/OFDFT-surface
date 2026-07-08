from ofks.config import load_system_config
from ofks.workflows.generate_references import generate_reference_structures


def test_generate_reference_structures_for_adsorption_system():
    config = load_system_config("configs/systems/mg0001_o_debug.yaml")

    atoms_list, records = generate_reference_structures(config, molecule_box_angstrom=10.0)

    assert len(atoms_list) == 2
    assert records[0]["reference_kind"] == "clean_slab"
    assert records[1]["reference_kind"] == "isolated_adsorbate"
    assert records[0]["adsorbate"] == "none"
    assert len(atoms_list[0]) == 12
    assert len(atoms_list[1]) == 1
    assert atoms_list[1].cell.lengths()[0] == 10.0
    assert records[0]["structure_id"] != records[1]["structure_id"]
