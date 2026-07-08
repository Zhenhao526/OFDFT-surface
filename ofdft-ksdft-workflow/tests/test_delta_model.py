import numpy as np

from ofks.models.delta import build_training_data, train_delta_model
from ofks.workflows.train_delta import add_predictions


def _record(structure_id: str, fast: float, ks: float, site: str = "fcc"):
    return {
        "structure_id": structure_id,
        "ks_status": "parsed_converged",
        "ks_total_energy_ev": ks,
        "total_energy_ev": fast,
        "height_angstrom": 2.4,
        "max_force_ev_per_ang": 0.01,
        "system_name": "toy",
        "adsorbate": "H",
        "site": site,
        "orientation": "atom",
    }


def test_build_training_data_uses_only_parsed_converged_records():
    records = [_record("a", -1.0, -3.0), {"ks_status": "output_missing", "total_energy_ev": -1.0}]

    usable, y = build_training_data(records)

    assert len(usable) == 1
    assert y.tolist() == [-2.0]


def test_build_training_data_skips_nonconverged_candidate_records():
    bad = _record("bad", -1.0, -3.0)
    bad["candidate_converged"] = False
    good = _record("good", -2.0, -4.0)

    usable, y = build_training_data([bad, good])

    assert [record["structure_id"] for record in usable] == ["good"]
    assert y.tolist() == [-2.0]


def test_train_delta_model_predicts_training_records():
    records = [
        _record("a", -1.0, -3.0, site="fcc"),
        _record("b", -2.0, -4.2, site="hcp"),
        _record("c", -3.0, -5.4, site="top"),
    ]

    model, metrics = train_delta_model(records, ridge_alpha=0.0)
    predictions = model.predict(records)
    _, y = build_training_data(records)

    assert metrics["n_records_trainable"] == 3
    assert np.allclose(predictions, y)


def test_add_predictions_adds_corrected_energy():
    records = [_record("a", -1.0, -3.0)]
    model, _ = train_delta_model(records, ridge_alpha=1.0)

    predicted = add_predictions(records, model)

    assert "delta_energy_pred_ev" in predicted[0]
    assert "corrected_total_energy_ev" in predicted[0]


def test_train_delta_model_can_target_adsorption_energy():
    records = [_record("a", -1.0, -3.0), _record("b", -2.0, -4.0)]
    for record in records:
        record["adsorption_energy_ev"] = record["total_energy_ev"] + 10.0
        record["ks_adsorption_energy_ev"] = record["ks_total_energy_ev"] + 10.0

    model, metrics = train_delta_model(
        records,
        truth_energy_key="ks_adsorption_energy_ev",
        candidate_energy_key="adsorption_energy_ev",
        corrected_energy_key="corrected_adsorption_energy_ev",
        delta_key="delta_adsorption_energy_pred_ev",
    )
    predicted = add_predictions(records, model)

    assert metrics["candidate_energy_key"] == "adsorption_energy_ev"
    assert "delta_adsorption_energy_pred_ev" in predicted[0]
    assert "corrected_adsorption_energy_ev" in predicted[0]
