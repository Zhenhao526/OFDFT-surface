# KSDFT Ground-Truth Benchmark Protocol

Date: 2026-07-07

## Objective

Use converged KSDFT as the internal ground truth, then compare candidate algorithms such as OFDFT, M-OFDFT, delta-corrected OFDFT, and fast surrogate models on the same structure set.

## Reference Definition

The reference label for each `structure_id` is a parsed QE/KSDFT result:

- `ks_total_energy_ev`
- `ks_forces_ev_per_ang`
- `ks_max_force_ev_per_ang`
- `qe_runtime_seconds` or `ks_runtime_seconds`, when available
- `ks_status = parsed_converged`

For adsorption studies, total-energy metrics should eventually be complemented by adsorption-energy metrics using consistent clean-slab and isolated-adsorbate references.

## Candidate Algorithm Contract

Each candidate algorithm output should be JSONL with one record per `structure_id`.

Recommended fields:

- `structure_id`
- `total_energy_ev` or `corrected_total_energy_ev`
- `forces_ev_per_ang`, optional
- `max_force_ev_per_ang`, optional
- `runtime_seconds`
- `backend`, for example `ofdft`, `m_ofdft`, `delta_ofdft`, or `surrogate`

KSDFT-like candidate records can also use the `ks_*` fields.

## Metrics

Energy:

- raw MAE/RMSE against KSDFT
- mean signed offset
- offset-aligned MAE/RMSE
- max absolute error

Ranking:

- Spearman correlation
- top-1 match
- top-3 recall

Force:

- atomwise force-vector MAE/RMSE, when vectors are available
- max-force MAE/RMSE

Time:

- candidate total runtime
- candidate median runtime
- KSDFT total runtime, when available
- speedup versus KSDFT

## Minimum Dataset Sizes

- Smoke: 1-3 structures, verifies execution and parsing only.
- Debug benchmark: 10-20 structures, checks ranking and rough error bars.
- Local scientific benchmark: 50-100 structures, enough for site/height ranking statistics.
- Production benchmark: 200+ structures across systems, enough to compare algorithm families.

## Current CLI

Example:

```bash
PYTHONPATH=src .venv/bin/python -m ofks.workflows.benchmark_algorithms \
  --truth data/processed/labels/mg0001_o_smoke_ks_parsed.jsonl \
  --candidate ksdft_self=data/processed/labels/mg0001_o_smoke_ks_parsed.jsonl \
  --candidate fake_fast=data/processed/screens/mg0001_o_smoke_fast.jsonl \
  --out-json data/reports/benchmarks/mg0001_o_smoke_benchmark.json \
  --out-md data/reports/benchmarks/mg0001_o_smoke_benchmark.md \
  --out-csv data/reports/benchmarks/mg0001_o_smoke_benchmark.csv \
  --truth-name ksdft_qe_pbe_smoke
```

## Next Implementation Step

Parse KSDFT labels from `qe_run_results.jsonl` after QE execution so `qe_runtime_seconds` is preserved in the benchmark table. The next practical run is a 10-structure debug benchmark with reduced local KSDFT settings before moving production labels to parallel hardware.
