import pytest

from ofks.workflows.build_anchored_kedf_adsorption import (
    build_anchored_kedf_adsorption_records,
    render_anchored_kedf_report,
)


def test_build_anchored_kedf_adsorption_records_calibrate_mu_o_from_ks_anchor():
    result = build_anchored_kedf_adsorption_records(
        truth_records=[{"structure_id": "anchor", "ks_adsorption_energy_ev": -2.0, "site": "top"}],
        candidate_records_by_name={
            "wt": [
                {"structure_id": "anchor", "total_energy_ev": -15.0, "converged": True, "runtime_seconds": 3.0},
                {"structure_id": "other", "total_energy_ev": -14.0, "converged": True, "runtime_seconds": 4.0},
            ]
        },
        slab_reference_records_by_name={
            "wt": [{"structure_id": "slab", "total_energy_ev": -10.0, "converged": True, "runtime_seconds": 5.0}]
        },
        anchor_structure_id="anchor",
        clean_slab_id="slab",
    )

    records = {record["structure_id"]: record for record in result["candidates"]["wt"]}
    assert result["skipped"] == []
    assert result["calibrations"]["wt"]["anchor_delta_interface_energy_ev"] == pytest.approx(-5.0)
    assert result["calibrations"]["wt"]["mu_o_eff_ev"] == pytest.approx(-3.0)
    assert records["anchor"]["adsorption_energy_ev"] == pytest.approx(-2.0)
    assert records["other"]["adsorption_energy_ev"] == pytest.approx(-1.0)
    assert records["other"]["runtime_seconds"] == pytest.approx(6.5)
    assert records["other"]["metadata"]["mu_o_eff_ev"] == pytest.approx(-3.0)
    assert records["other"]["metadata"]["slab"]["structure_id"] == "slab"


def test_build_anchored_kedf_adsorption_records_skip_missing_anchor_candidate():
    result = build_anchored_kedf_adsorption_records(
        truth_records=[{"structure_id": "anchor", "ks_adsorption_energy_ev": -2.0}],
        candidate_records_by_name={"mgp": [{"structure_id": "other", "total_energy_ev": -14.0}]},
        slab_reference_records_by_name={"mgp": [{"structure_id": "slab", "total_energy_ev": -10.0}]},
        anchor_structure_id="anchor",
        clean_slab_id="slab",
    )

    assert result["candidates"] == {}
    assert result["skipped"] == [
        {"variant": "mgp", "reason": "missing anchor adsorbed structure_id=anchor"}
    ]


def test_render_anchored_kedf_report_blocks_12_structure_expansion():
    text = render_anchored_kedf_report(
        {"truth_name": "ks", "truth_records": 0, "truth_energy_records": 0, "algorithms": []},
        {
            "anchor": {
                "structure_id": "anchor",
                "truth_adsorption_key": "ks_adsorption_energy_ev",
                "truth_adsorption_energy_ev": -2.0,
                "site": "top",
                "height_angstrom": 2.0,
            },
            "calibrations": {
                "wt": {
                    "candidate_records": 1,
                    "anchor_delta_interface_energy_ev": -5.0,
                    "truth_adsorption_energy_ev": -2.0,
                    "mu_o_eff_ev": -3.0,
                }
            },
            "adsorption_sign_sanity": {
                "wt": {
                    "records": 1,
                    "negative_records": 0,
                    "nonnegative_records": 1,
                    "min_adsorption_energy_ev": 1.0,
                    "max_adsorption_energy_ev": 1.0,
                    "all_negative": False,
                }
            },
            "expansion_gate": {
                "passed": False,
                "passed_variants": [],
                "blocked_variants": ["wt"],
            },
            "skipped": [],
        },
    )

    assert "mu_O_eff" in text
    assert "block 12" in text
    assert "12-structure expansion is blocked" in text
