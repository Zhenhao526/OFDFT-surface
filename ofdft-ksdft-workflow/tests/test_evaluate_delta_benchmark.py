from ofks.workflows.evaluate_delta_benchmark import _candidate_view, split_train_test


def _record(index: int):
    return {
        "structure_id": f"s{index}",
        "ks_status": "parsed_converged",
        "ks_total_energy_ev": float(index),
        "total_energy_ev": float(index + 10),
        "corrected_total_energy_ev": float(index + 1),
        "runtime_seconds": 0.1,
        "site": "hcp",
        "orientation": "atom",
        "height_angstrom": 2.0,
    }


def test_split_train_test_leaves_holdout_records():
    train, test = split_train_test([_record(index) for index in range(5)], train_fraction=0.6)

    assert len(train) == 3
    assert len(test) == 2
    assert {record["structure_id"] for record in train}.isdisjoint(
        {record["structure_id"] for record in test}
    )


def test_split_train_test_skips_nonconverged_candidate_records():
    records = [_record(index) for index in range(4)]
    records[0]["candidate_converged"] = False

    train, test = split_train_test(records, train_fraction=0.5)

    ids = {record["structure_id"] for record in train + test}
    assert "s0" not in ids
    assert ids == {"s1", "s2", "s3"}


def test_split_train_test_can_use_adsorption_energy_keys():
    records = [_record(index) for index in range(3)]
    for record in records:
        record.pop("ks_total_energy_ev")
        record.pop("total_energy_ev")
        record["ks_adsorption_energy_ev"] = -1.0
        record["adsorption_energy_ev"] = -0.5

    train, test = split_train_test(
        records,
        train_fraction=0.5,
        truth_energy_key="ks_adsorption_energy_ev",
        candidate_energy_key="adsorption_energy_ev",
    )

    assert len(train) == 2
    assert len(test) == 1


def test_candidate_view_does_not_leak_ks_truth_energy():
    candidate = _candidate_view(_record(1), energy_key="corrected_total_energy_ev")

    assert candidate["corrected_total_energy_ev"] == 2.0
    assert "ks_total_energy_ev" not in candidate


def test_candidate_view_keeps_adsorption_energy_fields():
    record = _record(1)
    record["adsorption_energy_ev"] = -1.0

    candidate = _candidate_view(record, energy_key="adsorption_energy_ev")

    assert candidate["adsorption_energy_ev"] == -1.0
    assert "ks_total_energy_ev" not in candidate
