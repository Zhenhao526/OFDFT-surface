import pytest

from ofks.workflows.build_hybrid_adsorption import build_hybrid_adsorption_records, select_reference_record


def test_build_hybrid_adsorption_records_combines_mixed_component_energies():
    adsorbed = [
        {
            "structure_id": "ads-1",
            "system_name": "mg_o",
            "site": "top",
            "height_angstrom": 1.6,
            "backend": "dftpy",
            "converged": True,
            "total_energy_ev": -20.0,
            "runtime_seconds": 2.0,
            "metadata": {"kedf": "LMGP", "xc": "PBE"},
        }
    ]
    slab = [
        {
            "structure_id": "slab-1",
            "reference_kind": "clean_slab",
            "reference_id": "mg_slab",
            "backend": "dftpy",
            "converged": True,
            "total_energy_ev": -10.0,
            "runtime_seconds": 3.0,
            "metadata": {"kedf": "WT", "xc": "PBE"},
        }
    ]
    adsorbate = [
        {
            "structure_id": "o2-1",
            "reference_kind": "isolated_adsorbate",
            "reference_id": "o2",
            "backend": "m_ofdft",
            "candidate_name": "mofdft_o2",
            "converged": True,
            "total_energy_ev": -7.0,
            "runtime_seconds": 4.0,
            "metadata": {"model": "oxygen_mofdft"},
        }
    ]

    records = build_hybrid_adsorption_records(
        adsorbed,
        slab,
        adsorbate,
        candidate_name="mg_wt_o_mofdft",
        backend="hybrid_ofdft",
        adsorbed_source="mg_o_lmgp",
        slab_source="mg_wt",
        adsorbate_source="o_mofdft",
        adsorbate_reference_id="o2",
    )

    assert len(records) == 1
    record = records[0]
    assert record["backend"] == "hybrid_ofdft"
    assert record["candidate_name"] == "mg_wt_o_mofdft"
    assert record["adsorption_energy_ev"] == pytest.approx(-3.0)
    assert record["runtime_seconds"] == pytest.approx(9.0)
    assert record["converged"] is True
    assert record["metadata"]["components"]["slab"]["source"] == "mg_wt"
    assert record["metadata"]["components"]["slab"]["kedf"] == "WT"
    assert record["metadata"]["components"]["adsorbate"]["source"] == "o_mofdft"
    assert record["metadata"]["components"]["adsorbate"]["backend"] == "m_ofdft"


def test_build_hybrid_adsorption_records_marks_unknown_or_failed_convergence():
    records = build_hybrid_adsorption_records(
        adsorbed_records=[{"structure_id": "a", "total_energy_ev": -20.0, "converged": True}],
        slab_reference_records=[{"reference_kind": "clean_slab", "total_energy_ev": -10.0, "converged": False}],
        adsorbate_reference_records=[{"reference_kind": "isolated_adsorbate", "total_energy_ev": -7.0}],
        candidate_name="hybrid",
        backend="hybrid",
        adsorbed_source="ads",
        slab_source="slab",
        adsorbate_source="adsorbate",
    )

    assert records[0]["converged"] is False
    assert records[0]["runtime_seconds"] is None


def test_select_reference_record_requires_exact_match():
    records = [
        {"reference_kind": "clean_slab", "reference_id": "a", "total_energy_ev": -1.0},
        {"reference_kind": "clean_slab", "reference_id": "b", "total_energy_ev": -2.0},
    ]

    selected = select_reference_record(records, reference_kind="clean_slab", reference_id="b", role="slab")
    assert selected["total_energy_ev"] == -2.0

    with pytest.raises(ValueError, match="Expected exactly one slab reference"):
        select_reference_record(records, reference_kind="clean_slab", reference_id=None, role="slab")
