from pathlib import Path

from ase import Atoms
from ase.io import write

from ofks.workflows.parse_ks_outputs import overlay_records_by_structure_id, parse_ks_manifest


def test_parse_ks_manifest_updates_records(tmp_path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    fixture = Path("tests/fixtures/qe/pw.out").read_text()
    output = job_dir / "pw.out"
    output.write_text(fixture)
    records = [{"structure_id": "abc", "ks_job_dir": str(job_dir), "ks_status": "input_prepared"}]

    parsed = parse_ks_manifest(records)

    assert parsed[0]["ks_status"] == "parsed_converged"
    assert parsed[0]["ks_converged"] is True
    assert parsed[0]["ks_total_energy_ry"] == -16.0
    assert parsed[0]["ks_forces_ev_per_ang"] is not None


def test_parse_ks_manifest_marks_missing_outputs(tmp_path):
    records = [{"structure_id": "abc", "ks_job_dir": str(tmp_path / "missing"), "ks_status": "input_prepared"}]

    parsed = parse_ks_manifest(records)

    assert parsed[0]["ks_status"] == "output_missing"


def test_parse_ks_manifest_rejects_force_count_mismatch(tmp_path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    output = job_dir / "pw.out"
    output.write_text(Path("tests/fixtures/qe/pw.out").read_text())
    structure = job_dir / "structure.extxyz"
    write(structure, Atoms("H3", positions=[(0, 0, 0), (0, 0, 1), (0, 0, 2)]))
    records = [
        {
            "structure_id": "abc",
            "ks_job_dir": str(job_dir),
            "ks_structure": str(structure),
            "ks_status": "input_prepared",
        }
    ]

    parsed = parse_ks_manifest(records)

    assert parsed[0]["ks_status"] == "parse_inconsistent"
    assert "force_count_mismatch" in parsed[0]["ks_parse_inconsistency"]
    assert "ks_total_energy_ev" not in parsed[0]


def test_overlay_records_by_structure_id_merges_only_matching_records():
    manifest = [
        {"structure_id": "a", "ks_status": "input_prepared"},
        {"structure_id": "b", "ks_status": "input_prepared"},
    ]
    overlay = [
        {"structure_id": "a", "qe_runtime_seconds": 12.0},
        {"structure_id": "old", "qe_runtime_seconds": 99.0},
    ]

    merged = overlay_records_by_structure_id(manifest, [overlay])

    assert merged[0]["qe_runtime_seconds"] == 12.0
    assert "qe_runtime_seconds" not in merged[1]
