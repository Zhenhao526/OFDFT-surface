from pathlib import Path

from ofks.workflows.prepare_qe_runs import select_missing_jobs, write_qe_run_scripts


def test_select_missing_jobs_skips_existing_outputs(tmp_path):
    missing_dir = tmp_path / "missing"
    done_dir = tmp_path / "done"
    partial_dir = tmp_path / "partial"
    missing_dir.mkdir()
    done_dir.mkdir()
    partial_dir.mkdir()
    (done_dir / "pw.out").write_text("JOB DONE.")
    (partial_dir / "pw.out").write_text("iteration #  1")
    records = [
        {"structure_id": "a", "ks_status": "output_missing", "ks_job_dir": str(missing_dir)},
        {"structure_id": "b", "ks_status": "output_missing", "ks_job_dir": str(done_dir)},
        {"structure_id": "c", "ks_status": "output_missing", "ks_job_dir": str(partial_dir)},
        {"structure_id": "d", "ks_status": "parsed_converged", "ks_job_dir": str(tmp_path / "parsed")},
    ]

    missing = select_missing_jobs(records)

    assert [record["structure_id"] for record in missing] == ["a", "c"]


def test_select_missing_jobs_retries_parse_inconsistent_outputs(tmp_path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    (job_dir / "pw.out").write_text("JOB DONE.")
    records = [
        {
            "structure_id": "bad",
            "ks_status": "parse_inconsistent",
            "ks_job_dir": str(job_dir),
        }
    ]

    assert select_missing_jobs(records) == records


def test_write_qe_run_scripts_creates_job_and_master_scripts(tmp_path):
    job_dir = tmp_path / "job"
    records = [{"structure_id": "a", "ks_status": "output_missing", "ks_job_dir": str(job_dir)}]
    master = tmp_path / "run_missing_qe.sh"

    write_qe_run_scripts(records, script_out=master, pw_command="pw.x")

    assert master.exists()
    assert job_dir.joinpath("run_qe.sh").exists()
    assert "pw.x -in pw.in > pw.out" in job_dir.joinpath("run_qe.sh").read_text()
    assert "./run_qe.sh" in master.read_text()
