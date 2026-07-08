from ofks.workflows.merge_candidate_labels import merge_candidate_labels


def test_merge_candidate_labels_preserves_ks_truth_and_overlays_candidate():
    truth = [
        {
            "structure_id": "a",
            "ks_status": "parsed_converged",
            "ks_total_energy_ev": -10.0,
            "total_energy_ev": 1.0,
        }
    ]
    candidate = [
        {
            "structure_id": "a",
            "backend": "dftpy",
            "converged": True,
            "total_energy_ev": -9.5,
            "adsorption_energy_ev": -1.5,
            "max_force_ev_per_ang": 2.0,
            "runtime_seconds": 3.0,
            "metadata": {"density_iterations": 42},
        }
    ]

    merged = merge_candidate_labels(truth, candidate, candidate_name="dftpy")

    assert len(merged) == 1
    assert merged[0]["ks_total_energy_ev"] == -10.0
    assert merged[0]["total_energy_ev"] == -9.5
    assert merged[0]["adsorption_energy_ev"] == -1.5
    assert merged[0]["candidate_converged"] is True
    assert merged[0]["candidate_metadata"]["density_iterations"] == 42
