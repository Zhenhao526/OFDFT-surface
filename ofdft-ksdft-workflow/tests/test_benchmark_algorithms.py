import json

import pytest

from ofks.benchmarks.ks_reference import build_benchmark_report, render_benchmark_markdown, write_summary_csv


def test_benchmark_reports_raw_and_offset_aligned_energy_errors(tmp_path):
    truth = [
        {
            "structure_id": "a",
            "ks_total_energy_ev": 10.0,
            "ks_forces_ev_per_ang": [[0.0, 0.0, 0.0]],
            "ks_max_force_ev_per_ang": 0.0,
            "qe_runtime_seconds": 10.0,
        },
        {
            "structure_id": "b",
            "ks_total_energy_ev": 12.0,
            "ks_forces_ev_per_ang": [[1.0, 0.0, 0.0]],
            "ks_max_force_ev_per_ang": 1.0,
            "qe_runtime_seconds": 20.0,
        },
        {
            "structure_id": "c",
            "ks_total_energy_ev": 11.0,
            "ks_forces_ev_per_ang": [[0.0, 1.0, 0.0]],
            "ks_max_force_ev_per_ang": 1.0,
            "qe_runtime_seconds": 30.0,
        },
    ]
    shifted = [
        {
            "structure_id": "a",
            "total_energy_ev": 110.0,
            "forces_ev_per_ang": [[0.0, 0.0, 0.0]],
            "max_force_ev_per_ang": 0.0,
            "runtime_seconds": 1.0,
        },
        {
            "structure_id": "b",
            "total_energy_ev": 112.0,
            "forces_ev_per_ang": [[1.1, 0.0, 0.0]],
            "max_force_ev_per_ang": 1.1,
            "runtime_seconds": 2.0,
        },
        {
            "structure_id": "c",
            "total_energy_ev": 111.0,
            "forces_ev_per_ang": [[0.0, 1.2, 0.0]],
            "max_force_ev_per_ang": 1.2,
            "runtime_seconds": 3.0,
        },
    ]

    report = build_benchmark_report(truth, {"shifted": shifted})
    metrics = report["algorithms"][0]

    assert metrics["energy_raw_mae_ev"] == pytest.approx(100.0)
    assert metrics["energy_offset_ev"] == pytest.approx(100.0)
    assert metrics["energy_aligned_mae_ev"] == pytest.approx(0.0)
    assert metrics["spearman_energy"] == pytest.approx(1.0)
    assert metrics["top1_match"] is True
    assert metrics["force_vector_mae_ev_per_ang"] == pytest.approx(0.1)
    assert metrics["max_force_mae_ev_per_ang"] == pytest.approx(0.1)
    assert metrics["speedup_vs_truth"] == pytest.approx(10.0)

    markdown = render_benchmark_markdown(report)
    assert "KSDFT Benchmark" in markdown
    assert "shifted" in markdown

    csv_path = tmp_path / "summary.csv"
    write_summary_csv(report, csv_path)
    csv_text = csv_path.read_text()
    assert "energy_aligned_mae_ev" in csv_text
    assert "\r\n" not in csv_text

    json.dumps(report)


def test_benchmark_marks_bad_top1_ranking():
    truth = [
        {"structure_id": "a", "ks_total_energy_ev": 0.0},
        {"structure_id": "b", "ks_total_energy_ev": 1.0},
    ]
    candidate = [
        {"structure_id": "a", "total_energy_ev": 2.0},
        {"structure_id": "b", "total_energy_ev": 1.0},
    ]

    report = build_benchmark_report(truth, {"bad_rank": candidate})
    metrics = report["algorithms"][0]

    assert metrics["top1_match"] is False
    assert metrics["spearman_energy"] == pytest.approx(-1.0)


def test_benchmark_does_not_treat_inherited_fast_runtime_as_ks_runtime():
    truth = [
        {
            "structure_id": "a",
            "ks_total_energy_ev": 10.0,
            "runtime_seconds": 0.001,
        }
    ]
    candidate = [
        {
            "structure_id": "a",
            "ks_total_energy_ev": 10.0,
            "runtime_seconds": 0.001,
        }
    ]

    report = build_benchmark_report(truth, {"ks_without_runtime": candidate})
    metrics = report["algorithms"][0]

    assert "truth_runtime_total_seconds" not in metrics
    assert "candidate_runtime_total_seconds" not in metrics
    assert "speedup_vs_truth" not in metrics


def test_benchmark_prefers_corrected_candidate_energy_over_inherited_ks_energy():
    truth = [{"structure_id": "a", "ks_total_energy_ev": 10.0}]
    candidate = [
        {
            "structure_id": "a",
            "ks_total_energy_ev": 10.0,
            "corrected_total_energy_ev": 12.0,
            "total_energy_ev": 20.0,
        }
    ]

    report = build_benchmark_report(truth, {"delta": candidate})
    metrics = report["algorithms"][0]

    assert metrics["energy_raw_mae_ev"] == pytest.approx(2.0)
    assert metrics["energy_raw_mean_signed_error_ev"] == pytest.approx(2.0)


def test_benchmark_reports_candidate_convergence_counts():
    truth = [{"structure_id": "a", "ks_total_energy_ev": 0.0}, {"structure_id": "b", "ks_total_energy_ev": 1.0}]
    candidate = [
        {"structure_id": "a", "total_energy_ev": 0.0, "converged": True},
        {"structure_id": "b", "total_energy_ev": 1.0, "converged": False},
    ]

    report = build_benchmark_report(truth, {"mixed": candidate})
    metrics = report["algorithms"][0]

    assert metrics["candidate_converged_records"] == 1
    assert metrics["matched_candidate_converged"] == 1
    assert "Candidate converged records: 1" in render_benchmark_markdown(report)


def test_benchmark_reports_adsorption_energy_metrics_when_present():
    truth = [
        {"structure_id": "a", "ks_total_energy_ev": 0.0, "ks_adsorption_energy_ev": -1.0},
        {"structure_id": "b", "ks_total_energy_ev": 1.0, "ks_adsorption_energy_ev": -2.0},
    ]
    candidate = [
        {"structure_id": "a", "total_energy_ev": 0.0, "adsorption_energy_ev": -0.5},
        {"structure_id": "b", "total_energy_ev": 1.0, "adsorption_energy_ev": -1.5},
    ]

    report = build_benchmark_report(truth, {"ads": candidate})
    metrics = report["algorithms"][0]

    assert metrics["adsorption_energy_raw_mae_ev"] == 0.5
    assert "adsorption_energy_aligned_mae_ev" in metrics


def test_benchmark_summary_falls_back_to_adsorption_metrics():
    truth = [
        {"structure_id": "a", "ks_adsorption_energy_ev": -1.0, "qe_runtime_seconds": 10.0},
        {"structure_id": "b", "ks_adsorption_energy_ev": -2.0, "qe_runtime_seconds": 20.0},
    ]
    candidate = [
        {"structure_id": "a", "adsorption_energy_ev": -0.5, "runtime_seconds": 1.0},
        {"structure_id": "b", "adsorption_energy_ev": -1.5, "runtime_seconds": 2.0},
    ]

    report = build_benchmark_report(truth, {"ads_only": candidate})
    markdown = render_benchmark_markdown(report)

    assert "adsorption raw MAE" in markdown
    assert "| ads_only | 2 |  |  | 0.5 | 0 | 1 | yes | 3 | 10 |" in markdown


def test_benchmark_summary_shows_adsorption_metrics_next_to_energy_metrics():
    truth = [
        {"structure_id": "a", "ks_total_energy_ev": 0.0, "ks_adsorption_energy_ev": -1.0},
        {"structure_id": "b", "ks_total_energy_ev": 1.0, "ks_adsorption_energy_ev": -2.0},
    ]
    candidate = [
        {"structure_id": "a", "total_energy_ev": 10.0, "adsorption_energy_ev": -0.5},
        {"structure_id": "b", "total_energy_ev": 11.0, "adsorption_energy_ev": -1.5},
    ]

    report = build_benchmark_report(truth, {"ads": candidate})
    markdown = render_benchmark_markdown(report)

    assert "adsorption raw MAE" in markdown
    assert "| ads | 2 | 10 | 0 | 0.5 | 0 | 1 | yes |" in markdown
