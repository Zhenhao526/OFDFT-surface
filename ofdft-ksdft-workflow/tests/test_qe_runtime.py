import os
from pathlib import Path

from ofks.calculators.qe_runtime import check_qe_environment, ensure_job_pseudo_link, run_qe_jobs


def test_check_qe_environment_detects_command_and_pseudos(tmp_path):
    fake_pw = tmp_path / "pw.x"
    fake_pw.write_text("#!/usr/bin/env bash\nexit 0\n")
    os.chmod(fake_pw, 0o755)
    pseudo = tmp_path / "pseudo"
    pseudo.mkdir()
    (pseudo / "H.UPF").write_text("pseudo")
    config = {
        "backend": "qe",
        "pseudo_dir": "pseudo",
        "pseudopotentials": {"H": "H.UPF", "O": "O.UPF"},
    }

    check = check_qe_environment(config, pw_command=str(fake_pw), base_dir=tmp_path)

    assert check.command_ok
    assert check.pseudo_dir_exists
    assert check.missing_pseudopotentials == ["O.UPF"]
    assert not check.ok


def test_run_qe_jobs_with_fake_executable(tmp_path):
    fake_pw = tmp_path / "pw.x"
    fake_pw.write_text(
        "#!/usr/bin/env bash\n"
        "echo 'fake qe run'\n"
        "echo 'JOB DONE.'\n"
    )
    os.chmod(fake_pw, 0o755)
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    (job_dir / "pw.in").write_text("&CONTROL\n/\n")
    records = [{"structure_id": "abc", "ks_job_dir": str(job_dir), "ks_status": "output_missing"}]

    results = run_qe_jobs(records, pw_command=str(fake_pw))

    assert results[0]["qe_run_status"] == "exit_0"
    assert results[0]["qe_returncode"] == 0
    assert (job_dir / "pw.out").read_text().splitlines() == ["fake qe run", "JOB DONE."]


def test_run_qe_jobs_resolves_relative_executable_before_changing_to_job_dir(tmp_path, monkeypatch):
    fake_pw = tmp_path / "pw.x"
    fake_pw.write_text("#!/usr/bin/env bash\necho 'ran from fake pw'\n")
    os.chmod(fake_pw, 0o755)
    job_dir = tmp_path / "nested" / "job"
    job_dir.mkdir(parents=True)
    (job_dir / "pw.in").write_text("&CONTROL\n/\n")
    records = [{"structure_id": "abc", "ks_job_dir": str(job_dir), "ks_status": "output_missing"}]
    monkeypatch.chdir(tmp_path)

    results = run_qe_jobs(records, pw_command="./pw.x")

    assert results[0]["qe_run_status"] == "exit_0"
    assert (job_dir / "pw.out").read_text().strip() == "ran from fake pw"


def test_run_qe_jobs_marks_missing_command(tmp_path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    records = [{"structure_id": "abc", "ks_job_dir": str(job_dir), "ks_status": "output_missing"}]

    results = run_qe_jobs(records, pw_command=str(tmp_path / "missing_pw.x"))

    assert results[0]["qe_run_status"] == "command_missing"


def test_run_qe_jobs_links_pseudo_source_before_execution(tmp_path):
    fake_pw = tmp_path / "pw.x"
    fake_pw.write_text("#!/usr/bin/env bash\nls pseudo/H.UPF\n")
    os.chmod(fake_pw, 0o755)
    pseudo_source = tmp_path / "shared_pseudo"
    pseudo_source.mkdir()
    (pseudo_source / "H.UPF").write_text("pseudo")
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    (job_dir / "pw.in").write_text("&CONTROL\n/\n")
    records = [{"structure_id": "abc", "ks_job_dir": str(job_dir), "ks_status": "output_missing"}]

    results = run_qe_jobs(records, pw_command=str(fake_pw), pseudo_source=pseudo_source)

    assert results[0]["qe_run_status"] == "exit_0"
    assert (job_dir / "pseudo").is_symlink()
    assert "pseudo/H.UPF" in (job_dir / "pw.out").read_text()


def test_ensure_job_pseudo_link_reports_missing_source(tmp_path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()

    assert not ensure_job_pseudo_link(job_dir, tmp_path / "missing")
