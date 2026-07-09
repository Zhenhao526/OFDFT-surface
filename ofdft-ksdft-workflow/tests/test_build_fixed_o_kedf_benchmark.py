import pytest

from ofks.workflows.build_fixed_o_kedf_benchmark import build_fixed_o_kedf_benchmark_records


def test_build_fixed_o_kedf_benchmark_records_use_fixed_o_reference():
    result = build_fixed_o_kedf_benchmark_records(
        candidate_records_by_name={
            "lmgp": [
                {
                    "structure_id": "ads",
                    "site": "top",
                    "height_angstrom": 1.6,
                    "total_energy_ev": -20.0,
                    "converged": True,
                    "runtime_seconds": 2.0,
                    "metadata": {"kedf": "LMGP", "xc": "PBE"},
                }
            ]
        },
        slab_reference_records_by_name={
            "lmgp": [
                {
                    "structure_id": "slab",
                    "total_energy_ev": -10.0,
                    "converged": True,
                    "runtime_seconds": 3.0,
                    "metadata": {"kedf": "LMGP", "xc": "PBE"},
                }
            ]
        },
        adsorbate_reference_record={
            "reference_id": "o_cal",
            "reference_kind": "isolated_adsorbate",
            "total_energy_ev": -4.0,
            "converged": True,
            "runtime_seconds": 0.0,
        },
        clean_slab_id="slab",
    )

    records = result["candidates"]["lmgp"]
    assert result["skipped"] == []
    assert records[0]["adsorption_energy_ev"] == pytest.approx(-6.0)
    assert records[0]["converged"] is True
    assert records[0]["runtime_seconds"] == pytest.approx(5.0)
    assert records[0]["metadata"]["adsorbate"]["reference_id"] == "o_cal"
    assert records[0]["metadata"]["slab"]["kedf"] == "LMGP"


def test_build_fixed_o_kedf_benchmark_records_skip_missing_slab_reference():
    result = build_fixed_o_kedf_benchmark_records(
        candidate_records_by_name={"mgp": [{"structure_id": "ads", "total_energy_ev": -20.0}]},
        slab_reference_records_by_name={},
        adsorbate_reference_record={"total_energy_ev": -4.0, "converged": True},
        clean_slab_id="slab",
    )

    assert result["candidates"] == {}
    assert result["skipped"] == [{"variant": "mgp", "reason": "missing slab-reference input"}]
