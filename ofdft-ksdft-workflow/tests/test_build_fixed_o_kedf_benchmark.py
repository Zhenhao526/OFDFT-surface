import pytest

from ofks.workflows.build_fixed_o_kedf_benchmark import (
    _adsorption_sign_sanity,
    build_fixed_o_kedf_benchmark_records,
    render_fixed_o_report,
)


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


def test_build_fixed_o_kedf_benchmark_records_sum_available_runtimes():
    result = build_fixed_o_kedf_benchmark_records(
        candidate_records_by_name={
            "wt": [
                {
                    "structure_id": "ads",
                    "total_energy_ev": -20.0,
                    "converged": True,
                    "runtime_seconds": 7.0,
                }
            ]
        },
        slab_reference_records_by_name={
            "wt": [
                {
                    "structure_id": "slab",
                    "total_energy_ev": -10.0,
                    "converged": True,
                    "runtime_seconds": 3.0,
                }
            ]
        },
        adsorbate_reference_record={"total_energy_ev": -4.0, "converged": True},
        clean_slab_id="slab",
    )

    assert result["candidates"]["wt"][0]["runtime_seconds"] == pytest.approx(10.0)


def test_build_fixed_o_kedf_benchmark_records_amortize_reference_runtime():
    result = build_fixed_o_kedf_benchmark_records(
        candidate_records_by_name={
            "wt": [
                {"structure_id": "ads1", "total_energy_ev": -20.0, "runtime_seconds": 10.0},
                {"structure_id": "ads2", "total_energy_ev": -21.0, "runtime_seconds": 20.0},
            ]
        },
        slab_reference_records_by_name={
            "wt": [{"structure_id": "slab", "total_energy_ev": -10.0, "runtime_seconds": 4.0}]
        },
        adsorbate_reference_record={"total_energy_ev": -4.0},
        clean_slab_id="slab",
    )

    records = result["candidates"]["wt"]
    assert [record["runtime_seconds"] for record in records] == pytest.approx([12.0, 22.0])
    assert sum(record["runtime_seconds"] for record in records) == pytest.approx(34.0)


def test_adsorption_sign_sanity_flags_nonnegative_records():
    summary = _adsorption_sign_sanity(
        {
            "wt": [
                {"adsorption_energy_ev": -1.0},
                {"adsorption_energy_ev": 0.0},
                {"adsorption_energy_ev": 2.0},
            ]
        }
    )

    assert summary["wt"]["negative_records"] == 1
    assert summary["wt"]["nonnegative_records"] == 2
    assert summary["wt"]["all_negative"] is False


def test_render_fixed_o_report_includes_sign_sanity_warning():
    text = render_fixed_o_report(
        {"truth_name": "ks", "truth_records": 0, "truth_energy_records": 0, "algorithms": []},
        {
            "adsorbate_reference": {"reference_id": "o", "total_energy_ev": -1.0},
            "adsorption_sign_sanity": {
                "wt": {
                    "records": 1,
                    "negative_records": 0,
                    "nonnegative_records": 1,
                    "min_adsorption_energy_ev": 2.0,
                    "max_adsorption_energy_ev": 2.0,
                    "all_negative": False,
                }
            },
            "skipped": [],
        },
    )

    assert "nonphysical raw branch" in text
    assert "Warning:" in text
