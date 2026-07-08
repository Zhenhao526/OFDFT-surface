# OFDFT-Assisted KSDFT Workflow

This repository implements a reproducible workflow for simple-metal surface adsorption studies:

```text
candidate generation -> fast OFDFT/ML screening -> KSDFT validation -> delta-learning correction -> active learning
```

Phase 1 focuses on code infrastructure and structure generation for systems such as:

- `H/Al(111)`
- `H2O/Al(111)`
- `O/Mg(0001)`

The workflow is intentionally backend-neutral. DFTpy, Quantum ESPRESSO, VASP, GPAW, and ML force fields should be connected through calculator adapters.

## Quick Start

```bash
uv --cache-dir .uv-cache sync --extra dev
.venv/bin/ofks-generate --system configs/systems/al111_h2o.yaml --out data/processed/structures/al111_h2o_candidates.extxyz
.venv/bin/ofks-fast-screen --structures data/processed/structures/al111_h2o_candidates.extxyz --calculator configs/calculators/fake_fast.yaml --out data/raw/fake/al111_h2o_screen.jsonl
.venv/bin/ofks-active-select --pool data/raw/fake/al111_h2o_screen.jsonl --budget 30 --out data/processed/splits/al111_h2o_ks_batch.jsonl
.venv/bin/ofks-ks-validate --selected data/processed/splits/al111_h2o_ks_batch.jsonl --structures data/processed/structures/al111_h2o_candidates.extxyz --calculator configs/calculators/qe_pbe.yaml --out data/raw/ksdft/al111_h2o
.venv/bin/ofks-parse-ks --manifest data/raw/ksdft/al111_h2o/manifest.jsonl --out data/processed/labels/al111_h2o_ks_parsed.jsonl
.venv/bin/ofks-train-delta --dataset data/processed/labels/al111_h2o_ks_parsed.jsonl --model-out data/processed/models/al111_h2o_delta.json --report data/reports/al111_h2o_delta.md --predictions-out data/processed/labels/al111_h2o_delta_pred.jsonl
.venv/bin/ofks-summarize --system al111_h2o --candidates data/processed/structures/al111_h2o_candidates.extxyz --fast-screen data/raw/fake/al111_h2o_screen.jsonl --selected data/processed/splits/al111_h2o_ks_batch.jsonl --manifest data/raw/ksdft/al111_h2o/manifest.jsonl --parsed data/processed/labels/al111_h2o_ks_parsed.jsonl --predictions data/processed/labels/al111_h2o_delta_pred.jsonl --delta-report data/reports/al111_h2o_delta.md --out data/reports/al111_h2o_summary.md
.venv/bin/ofks-prepare-qe-runs --records data/processed/labels/al111_h2o_ks_parsed.jsonl --script-out data/raw/ksdft/al111_h2o/run_missing_qe.sh --missing-out data/processed/splits/al111_h2o_missing_qe.jsonl
.venv/bin/ofks-check-qe-env --calculator configs/calculators/qe_pbe.yaml --base-dir .
.venv/bin/ofks-run-qe --records data/processed/splits/al111_h2o_missing_qe.jsonl --out data/raw/ksdft/al111_h2o/qe_run_results.jsonl --pseudo-source pseudo --limit 1
.venv/bin/pytest
```

If console scripts have not been regenerated after editing `pyproject.toml`, run modules directly during development:

```bash
PYTHONPATH=src .venv/bin/python -m ofks.workflows.run_fast_screen --structures data/processed/structures/al111_h2o_candidates.extxyz --calculator configs/calculators/fake_fast.yaml --out data/raw/fake/al111_h2o_screen.jsonl
PYTHONPATH=src .venv/bin/python -m ofks.workflows.active_select --pool data/raw/fake/al111_h2o_screen.jsonl --budget 30 --out data/processed/splits/al111_h2o_ks_batch.jsonl
PYTHONPATH=src .venv/bin/python -m ofks.workflows.run_ks_validation --selected data/processed/splits/al111_h2o_ks_batch.jsonl --structures data/processed/structures/al111_h2o_candidates.extxyz --calculator configs/calculators/qe_pbe.yaml --out data/raw/ksdft/al111_h2o
PYTHONPATH=src .venv/bin/python -m ofks.workflows.parse_ks_outputs --manifest data/raw/ksdft/al111_h2o/manifest.jsonl --out data/processed/labels/al111_h2o_ks_parsed.jsonl
PYTHONPATH=src .venv/bin/python -m ofks.workflows.train_delta --dataset data/processed/labels/al111_h2o_ks_parsed.jsonl --model-out data/processed/models/al111_h2o_delta.json --report data/reports/al111_h2o_delta.md --predictions-out data/processed/labels/al111_h2o_delta_pred.jsonl
PYTHONPATH=src .venv/bin/python -m ofks.workflows.summarize --system al111_h2o --candidates data/processed/structures/al111_h2o_candidates.extxyz --fast-screen data/raw/fake/al111_h2o_screen.jsonl --selected data/processed/splits/al111_h2o_ks_batch.jsonl --manifest data/raw/ksdft/al111_h2o/manifest.jsonl --parsed data/processed/labels/al111_h2o_ks_parsed.jsonl --predictions data/processed/labels/al111_h2o_delta_pred.jsonl --delta-report data/reports/al111_h2o_delta.md --out data/reports/al111_h2o_summary.md
PYTHONPATH=src .venv/bin/python -m ofks.workflows.prepare_qe_runs --records data/processed/labels/al111_h2o_ks_parsed.jsonl --script-out data/raw/ksdft/al111_h2o/run_missing_qe.sh --missing-out data/processed/splits/al111_h2o_missing_qe.jsonl
PYTHONPATH=src .venv/bin/python -m ofks.workflows.check_qe_env --calculator configs/calculators/qe_pbe.yaml --base-dir . --report-out data/reports/qe_env.md
PYTHONPATH=src .venv/bin/python -m ofks.workflows.run_qe_jobs --records data/processed/splits/al111_h2o_missing_qe.jsonl --out data/raw/ksdft/al111_h2o/qe_run_results.jsonl --pseudo-source pseudo --limit 1
```

## Current Status

Implemented:

- config loading
- slab construction
- adsorbate construction
- adsorption site enumeration
- candidate placement and deduplication
- deterministic structure hashing
- minimal `ofks-generate` CLI
- calculator adapter interface
- deterministic fake calculator
- minimal `ofks-fast-screen` CLI
- minimal `ofks-active-select` CLI
- minimal Quantum ESPRESSO input writer
- minimal `ofks-ks-validate` input preparation CLI
- Quantum ESPRESSO `pw.out` parser for energies, forces, and convergence
- minimal `ofks-parse-ks` CLI
- baseline ridge delta-learning model for energy correction
- minimal `ofks-train-delta` CLI
- Markdown workflow summary report
- minimal `ofks-summarize` CLI
- missing QE job list and run-script preparation
- minimal `ofks-prepare-qe-runs` CLI
- Quantum ESPRESSO environment checker
- real QE job runner for prepared calculation folders
- optional DFTpy-backed OFDFT runner
- KSDFT ground-truth benchmark report writer
- train/test delta benchmark workflow
- parsed QE runtime overlays after manifest regeneration
- DFTpy convergence sweep workflow
- KSDFT truth and candidate-output merge workflow for delta learning
- adsorption-energy field workflow and benchmark metrics when references are available
- clean-slab and isolated-adsorbate reference structure generator
- local `pylibxc.functional` compatibility shim for DFTpy/PBE debug runs
- adsorption-energy delta benchmark workflow against KSDFT ground truth
- formal batch status report workflow
- medium-size `Mg(0001)+O` pilot with 12 real QE/PBE scf labels and adsorption-energy benchmarks
- K-fold delta-learning cross-validation workflow
- DFTpy LDA/PBE comparison on the same pilot KSDFT labels for error-source diagnosis
- deterministic lateral-jitter candidate expansion and diverse structure sampling workflow
- active-selection exclusion of already labeled structures for iterative KSDFT rounds
- duplicate-protected JSONL record combination workflow for growing formal training sets
- expanded `Mg(0001)+O` pilot with 50 QE/PBE scf labels and final project report

Not yet implemented:

- production-grade DFTpy/PBE setup with validated OFDFT local pseudopotentials
- production M-OFDFT model training beyond the current linear delta-learning baseline
- complete production-scale 4x4x4 QE/PBE label set on parallel/HPC resources

Note: before real QE outputs exist, `ofks-parse-ks` marks records as `output_missing`.
If `pw.x` or the configured UPF files are unavailable, `ofks-check-qe-env` reports `Not ready` and `ofks-run-qe` records `command_missing` rather than silently succeeding.
When `--pseudo-source pseudo` is provided, each job receives a `pseudo/` symlink to the shared project pseudopotential directory before execution.
For OFDFT runs, install the optional dependency set with `uv sync --extra ofdft --extra dev`. The repository includes a narrow local `pylibxc.functional` compatibility shim for DFTpy/PBE debug runs against Homebrew `libxc`; production work should replace or harden that path and use validated OFDFT local pseudopotentials.
