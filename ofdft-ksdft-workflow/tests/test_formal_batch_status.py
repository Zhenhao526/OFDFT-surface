import json

from ofks.io import write_jsonl
from ofks.workflows.formal_batch_status import build_status_report


def test_formal_status_report_shows_incomplete_ks_batch(tmp_path):
    selected = tmp_path / "selected.jsonl"
    ks_labels = tmp_path / "ks.jsonl"
    missing = tmp_path / "missing.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    benchmark = tmp_path / "benchmark.json"

    write_jsonl(
        selected,
        [
            {"structure_id": "a"},
            {"structure_id": "b"},
        ],
    )
    write_jsonl(
        ks_labels,
        [
            {"structure_id": "a", "ks_status": "parsed_converged", "qe_runtime_seconds": 10.0},
            {"structure_id": "b", "ks_status": "output_missing"},
        ],
    )
    write_jsonl(missing, [{"structure_id": "b", "ks_status": "output_missing"}])
    write_jsonl(
        candidate,
        [
            {"structure_id": "a", "converged": True, "runtime_seconds": 1.0},
            {"structure_id": "b", "converged": False, "runtime_seconds": 2.0},
        ],
    )
    benchmark.write_text(
        json.dumps(
            {
                "algorithms": [
                    {
                        "name": "fast",
                        "n_matched": 1,
                        "energy_raw_mae_ev": 2.0,
                        "spearman_energy": 1.0,
                        "speedup_vs_truth": 10.0,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = build_status_report(
        system="toy",
        selected=selected,
        ks_labels=ks_labels,
        missing=missing,
        candidate_outputs={"fast": candidate},
        benchmarks=[benchmark],
    )

    assert "Parsed converged: 1/2 (50.0%)" in report
    assert "Missing QE jobs remain: 1" in report
    assert "| fast |" in report
