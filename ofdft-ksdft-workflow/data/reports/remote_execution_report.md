# Remote Execution Report

## Remote Workspace

- Host: `xiazhenhao@180.184.249.155:10086`
- Remote directory: `/mnt/afs/home/xiazhenhao/ofdft-ksdft-all50-20260708`
- Synced scope: source code, configs, pseudopotentials, processed labels/screens/reports, and lightweight QE runtime JSONL summaries.
- Excluded scope: local `.venv`, `_runtime`, caches, and the 10 GB `data/raw/ksdft/` QE work directories.

## Environment

- Python environment: `.venv-remote`
- Installer: `~/.local/bin/uv`
- Working install command used an independent project cache and Tsinghua PyPI mirror:
  - `UV_CACHE_DIR=.uv-cache-tuna UV_LINK_MODE=copy uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev,ofdft]" --python .venv-remote/bin/python`
- DFTpy: `2.2.0`
- LibXC source: `/mnt/afs/home/xiazhenhao/mamba-envs/abacus-mpn-gpu-ustc/lib/libxc.so`
- Runtime environment required for PBE/LibXC runs:
  - `LIBXC_LIBRARY_PATH=/mnt/afs/home/xiazhenhao/mamba-envs/abacus-mpn-gpu-ustc/lib/libxc.so`
  - `LD_LIBRARY_PATH=/mnt/afs/home/xiazhenhao/mamba-envs/abacus-mpn-gpu-ustc/lib:$LD_LIBRARY_PATH`

## Code Updates

- `src/pylibxc/functional.py`
  - Added `LIBXC_LIBRARY_PATH` and `LD_LIBRARY_PATH` discovery for Linux remote environments.
- `src/ofks/calculators/dftpy_runner.py`
  - Added `kedf_options` passthrough into DFTpy `KEDF` config.
- `src/ofks/workflows/sweep_dftpy_convergence.py`
  - Added MGP/MGPA/LMGP/LMGPA/HC/revHC smoke variants.
  - Added `--variant-filter` for targeted KEDF runs.
  - Changed JSONL writing to flush each record incrementally, preserving partial results if a variant times out.

## Verification

- Remote full test suite:
  - `65 passed, 10 warnings`
- Remote targeted tests after KEDF/sweep changes:
  - `8 passed, 10 warnings`

## all50 Reproduction

Remote reports:

- `data/reports/benchmarks/remote_all50_adsorption_benchmark.md`
- `data/reports/benchmarks/remote_all50_ads_cv/cv_report.md`

Key all50 metrics reproduced from synced results:

| method | matched | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | median runtime (s) | speedup vs QE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DFTpy/PBE/WT raw | 50 | 236.127 | 31.5988 | 0.152845 | 2.08225 | 63.7136 |
| DFTpy/PBE/WT + delta-CV | 50 | 0.325418 | 0.325418 | 0.827323 | 2.08225 | 63.7136 |

The reproduced values match the local all50 report. Note that these timings come from the previously completed DFTpy/QE records, not from a fresh remote DFTpy rerun.

## KEDF Smoke Results

Remote reports:

- `data/reports/benchmarks/remote_kedf_smoke_small_mgp.md`
- `data/reports/benchmarks/remote_kedf_smoke_small_wt_m30.md`
- `data/reports/benchmarks/remote_kedf_smoke_wt_mgp.jsonl`

Smoke system: `mg0001_o_smoke_candidates.extxyz`, first structure, 13 atoms, PBE XC, grid spacing 0.8 A.

| variant | status | converged | iterations | E (eV) | Fmax (eV/A) | remote runtime (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `mgp_atomic_sp08_m30` | ok | no | 30 | -23468.5 | 1058.35 | 155.687 |
| `wt_heg_sp08_m30` | ok | no | 30 | -23092.9 | 1316.94 | 180.13 |

Additional partial run on the 28-atom pilot structure:

| variant | status | converged | iterations | remote runtime (s) |
| --- | --- | --- | ---: | ---: |
| `wt_atomic_sp08_m100` | ok | yes | 41 | 270.633 |

Interpretation:

- MGP is runnable in the current DFTpy/QE-compatible environment.
- The current remote node was under heavy ABACUS compilation load during the smoke runs, so these fresh remote wall times should not be used as final speed benchmarks.
- Under this load, even WT slowed from the earlier recorded median 2.08 s/structure to hundreds of seconds for fresh runs.
- The next reliable KEDF comparison should be scheduled when the node is idle, or moved to a compute node/job allocation.

## Next Execution Path

1. Keep WT/PBE/delta-CV as the current baseline because all50 reproduction is complete.
2. Re-run KEDF smoke when the remote node is idle:
   - `wt_heg_sp08_m30`
   - `mgp_atomic_sp08_m30`
   - `mgpa_atomic_sp08_m30`
   - `lmgp_atomic_sp08_m30`
   - `lmgpa_atomic_sp08_m30`
   - `hc_atomic_sp08_m30`
   - `revhc_atomic_sp08_m30`
3. Promote only variants that finish and show stable behavior to 12-structure pilot screening.
4. For promoted variants, generate adsorption energies and compare against the existing all50 KSDFT truth with the same benchmark/delta-CV pipeline.
