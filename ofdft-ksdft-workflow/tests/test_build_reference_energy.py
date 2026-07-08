import pytest

from ofks.workflows.build_hybrid_adsorption import build_hybrid_adsorption_records
from ofks.workflows.build_reference_energy import build_reference_energy_record


def test_build_reference_energy_record_scales_molecular_reference():
    record = build_reference_energy_record(
        energy_ev=-12.0,
        energy_scale=0.5,
        reference_id="half_o2_mofdft",
        adsorbate="O",
        formula="O2",
        backend="mofdft",
        candidate_name="mofdft_o2_reference",
        method="m_ofdft",
        xc="PBE",
        reference_convention="half_o2",
        runtime_seconds=1.25,
    )

    assert record["reference_kind"] == "isolated_adsorbate"
    assert record["reference_id"] == "half_o2_mofdft"
    assert record["adsorbate"] == "O"
    assert record["total_energy_ev"] == pytest.approx(-6.0)
    assert record["converged"] is True
    assert record["runtime_seconds"] == pytest.approx(1.25)
    assert record["metadata"]["formula"] == "O2"
    assert record["metadata"]["input_energy_ev"] == pytest.approx(-12.0)
    assert record["metadata"]["energy_scale"] == pytest.approx(0.5)
    assert record["metadata"]["scaled_energy_ev"] == pytest.approx(-6.0)
    assert record["metadata"]["energy_shift_ev"] == pytest.approx(0.0)
    assert record["metadata"]["reference_convention"] == "half_o2"


def test_build_reference_energy_record_applies_calibration_shift():
    record = build_reference_energy_record(
        energy_ev=-12.0,
        energy_scale=0.5,
        energy_shift_ev=1.25,
        reference_id="half_o2_calibrated",
        formula="O2",
        reference_convention="half_o2_calibrated_to_qe_o_atom",
    )

    assert record["total_energy_ev"] == pytest.approx(-4.75)
    assert record["metadata"]["scaled_energy_ev"] == pytest.approx(-6.0)
    assert record["metadata"]["energy_shift_ev"] == pytest.approx(1.25)


def test_reference_energy_record_feeds_hybrid_adsorption_builder():
    adsorbate = build_reference_energy_record(
        energy_ev=-12.0,
        energy_scale=0.5,
        reference_id="half_o2_mofdft",
        adsorbate="O",
        formula="O2",
        backend="mofdft",
    )

    records = build_hybrid_adsorption_records(
        adsorbed_records=[{"structure_id": "ads", "total_energy_ev": -20.0, "converged": True}],
        slab_reference_records=[{"reference_kind": "clean_slab", "total_energy_ev": -10.0, "converged": True}],
        adsorbate_reference_records=[adsorbate],
        candidate_name="wt_mg_mofdft_o",
        backend="hybrid_ofdft",
        adsorbed_source="wt_adsorbed",
        slab_source="wt_slab",
        adsorbate_source="mofdft_half_o2",
        adsorbate_reference_id="half_o2_mofdft",
    )

    assert records[0]["adsorption_energy_ev"] == pytest.approx(-4.0)
    assert records[0]["metadata"]["components"]["adsorbate"]["source"] == "mofdft_half_o2"
    assert records[0]["metadata"]["components"]["adsorbate"]["backend"] == "mofdft"
