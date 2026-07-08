from ofks.reports.summary import build_summary, render_summary_markdown
from ofks.io import write_jsonl


def test_summary_report_counts_and_recommends_more_labels(tmp_path):
    fast = tmp_path / "fast.jsonl"
    selected = tmp_path / "selected.jsonl"
    parsed = tmp_path / "parsed.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    write_jsonl(
        fast,
        [
            {"structure_id": "a", "converged": True, "total_energy_ev": -1.0, "site": "fcc"},
            {"structure_id": "b", "converged": True, "total_energy_ev": -0.5, "site": "top"},
        ],
    )
    write_jsonl(selected, [{"structure_id": "a", "selection_reason": "best"}])
    write_jsonl(
        parsed,
        [
            {"structure_id": "a", "ks_status": "parsed_converged", "total_energy_ev": -1.0},
            {"structure_id": "b", "ks_status": "output_missing", "total_energy_ev": -0.5},
        ],
    )
    write_jsonl(predictions, [{"structure_id": "a", "corrected_total_energy_ev": -2.0, "site": "fcc"}])

    summary = build_summary(
        system="toy",
        fast_screen=fast,
        selected=selected,
        parsed=parsed,
        predictions=predictions,
    )
    text = render_summary_markdown(summary)

    assert summary.counts["fast_screen_records"] == 2
    assert summary.counts["parsed_converged"] == 1
    assert "Collect at least 5 parsed_converged KS labels" in text
    assert "Top Corrected Records" in text
