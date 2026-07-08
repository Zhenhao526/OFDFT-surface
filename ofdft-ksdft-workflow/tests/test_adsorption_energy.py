from ofks.metrics.adsorption import adsorption_energy


def test_adsorption_energy_formula():
    assert adsorption_energy(-15.0, -10.0, -3.0) == -2.0
