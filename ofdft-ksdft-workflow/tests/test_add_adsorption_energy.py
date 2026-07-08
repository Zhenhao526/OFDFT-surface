from ofks.workflows.add_adsorption_energy import add_adsorption_energy_fields


def test_add_adsorption_energy_fields_uses_selected_energy_key():
    records = [{"structure_id": "a", "ks_total_energy_ev": -15.0}, {"structure_id": "b"}]

    updated = add_adsorption_energy_fields(
        records,
        slab_energy_ev=-10.0,
        adsorbate_energy_ev=-3.0,
        energy_key="ks_total_energy_ev",
        out_key="ks_adsorption_energy_ev",
    )

    assert updated[0]["ks_adsorption_energy_ev"] == -2.0
    assert "ks_adsorption_energy_ev" not in updated[1]
