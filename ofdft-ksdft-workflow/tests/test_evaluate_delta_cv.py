from ofks.workflows.evaluate_delta_cv import run_delta_cv


def _record(index: int):
    return {
        "structure_id": f"s{index}",
        "ks_status": "parsed_converged",
        "ks_total_energy_ev": float(index),
        "total_energy_ev": float(index + 10),
        "ks_adsorption_energy_ev": float(index - 1),
        "adsorption_energy_ev": float(index + 9),
        "runtime_seconds": 0.1,
        "site": "top" if index % 2 else "fcc",
        "orientation": "atom",
        "height_angstrom": 2.0 + index * 0.1,
        "max_force_ev_per_ang": 1.0,
        "system_name": "toy",
        "adsorbate": "O",
    }


def test_delta_cv_covers_all_usable_records():
    result = run_delta_cv(
        [_record(index) for index in range(4)],
        folds=2,
        ridge_alpha=1.0,
        truth_name="ks",
        raw_name="raw",
        delta_name="delta",
        truth_energy_key="ks_total_energy_ev",
        candidate_energy_key="total_energy_ev",
        corrected_energy_key="corrected_total_energy_ev",
        delta_key="delta_energy_pred_ev",
    )

    assert len(result["folds"]) == 2
    assert len(result["raw_predictions"]) == 4
    assert len(result["delta_predictions"]) == 4
    assert result["benchmark"]["algorithms"][0]["n_matched"] == 4
    assert result["benchmark"]["algorithms"][1]["n_matched"] == 4


def test_delta_cv_can_target_adsorption_energy():
    result = run_delta_cv(
        [_record(index) for index in range(4)],
        folds=2,
        ridge_alpha=1.0,
        truth_name="ks_ads",
        raw_name="raw_ads",
        delta_name="delta_ads",
        truth_energy_key="ks_adsorption_energy_ev",
        candidate_energy_key="adsorption_energy_ev",
        corrected_energy_key="corrected_adsorption_energy_ev",
        delta_key="delta_adsorption_energy_pred_ev",
    )

    delta_algo = result["benchmark"]["algorithms"][1]
    assert delta_algo["n_matched"] == 4
    assert "adsorption_energy_raw_mae_ev" in delta_algo
