from ofks.workflows.active_select import select_records


def test_active_select_prefers_diverse_low_energy_records():
    records = [
        {"structure_id": "a", "converged": True, "total_energy_ev": -3.0, "site": "top", "orientation": "flat"},
        {"structure_id": "b", "converged": True, "total_energy_ev": -2.9, "site": "top", "orientation": "flat"},
        {"structure_id": "c", "converged": True, "total_energy_ev": -2.8, "site": "fcc", "orientation": "flat"},
        {"structure_id": "d", "converged": False, "total_energy_ev": -10.0, "site": "hcp", "orientation": "flat"},
    ]

    selected = select_records(records, budget=3)

    assert [record["structure_id"] for record in selected] == ["a", "c", "b"]
    assert selected[0]["selection_reason"] == "best_in_site_orientation_group"
    assert selected[-1]["selection_reason"] == "low_energy_fill"


def test_active_select_excludes_existing_structure_ids():
    records = [
        {"structure_id": "a", "converged": True, "total_energy_ev": -3.0, "site": "top", "orientation": "flat"},
        {"structure_id": "b", "converged": True, "total_energy_ev": -2.9, "site": "top", "orientation": "flat"},
        {"structure_id": "c", "converged": True, "total_energy_ev": -2.8, "site": "fcc", "orientation": "flat"},
    ]

    selected = select_records(records, budget=3, excluded_ids={"a"})

    assert [record["structure_id"] for record in selected] == ["b", "c"]
