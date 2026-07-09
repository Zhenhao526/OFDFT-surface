# First4 Fixed-O KEDF Adsorption Benchmark Summary

## Scope

- System: Mg(0001)+O, first 4 pilot adsorbed structures.
- Structures: top 1.6 A, top 2.0 A, top 2.4 A, bridge 1.6 A.
- Truth: `data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl`.
- Adsorbate reference: calibrated atomic O, `E(O) = -559.8598218127081 eV`.
- Formula: `E_ads = E_KEDF(slab+O) - E_KEDF(clean slab) - E_fixed(O)`.
- O atom is treated as an atomic-O branch, not as `1/2 O2`.

## Remote Runs

- Clean slab references: `data/reports/benchmarks/remote_kedf_missing_refs_libxc_20260709_1055`.
- Adsorbed structures: `data/reports/benchmarks/remote_kedf_adsorbed_first4_libxc_20260709_1101`.
- Required environment:
  - `LIBXC_LIBRARY_PATH=/mnt/afs/home/xiazhenhao/mamba-envs/abacus-mpn-gpu-ustc/lib/libxc.so`
  - `LD_LIBRARY_PATH=/mnt/afs/home/xiazhenhao/mamba-envs/abacus-mpn-gpu-ustc/lib:$LD_LIBRARY_PATH`
- A first attempt without those LibXC variables produced error records and is not used for the benchmark.

## Adsorption Error Ranking

Ranked by raw adsorption MAE against KSDFT:

| rank | KEDF variant | matched | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | runtime total (s) |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `mgpa_atomic_sp08_m30` | 4 | 36.204 | 35.697 | 0.0 | 777.822 |
| 2 | `wt_heg_sp08_m30` | 4 | 59.312 | 37.103 | 0.6 | 636.434 |
| 3 | `mgp_atomic_sp08_m30` | 4 | 94.167 | 34.630 | 0.0 | 716.615 |
| 4 | `tf_heg_sp08_m100` | 4 | 122.959 | 13.169 | 0.0 | 1319.847 |
| 5 | `lmgp_atomic_sp08_m30` | 4 | 123.245 | 14.249 | 0.0 | 743.946 |
| 6 | `hc_atomic_sp08_m30` | 4 | 127.561 | 13.282 | 0.0 | 540.139 |
| 7 | `revhc_atomic_sp08_m30` | 4 | 127.905 | 9.608 | 0.0 | 602.510 |
| 8 | `lmgpa_atomic_sp08_m30` | 4 | 149.012 | 11.029 | 0.0 | 510.260 |
| 9 | `tfvw_heg_sp08_m100` | 4 | 179.292 | 6.116 | 0.6 | 473.859 |

## Interpretation

- Raw adsorption MAE is still large for every KEDF. On this four-structure subset, MGPA is the best raw candidate, followed by WT.
- Several methods have small aligned MAE after removing a constant adsorption offset, especially TFvW, revHC, LMGPA, TF, HC, and LMGP. This suggests some errors are offset-like on this tiny subset, but it is not yet a reliable ranking result.
- Spearman is mostly 0 with only 4 structures. Treat ranking/top-k metrics as diagnostic only.
- Runtime totals include four adsorbed calculations plus one clean slab reference per variant. These fresh remote timings were collected on a busy login node and should not replace a controlled speed benchmark.

## Next Step

Promote a smaller set to 12-structure pilot runs:

- Keep raw-MAE baselines: `mgpa_atomic_sp08_m30`, `wt_heg_sp08_m30`, `mgp_atomic_sp08_m30`.
- Keep offset-shape candidates: `revhc_atomic_sp08_m30`, `hc_atomic_sp08_m30`, `lmgp_atomic_sp08_m30`.
- Deprioritize `tfvw_heg_sp08_m100` for raw adsorption energy despite its low aligned MAE, because its raw adsorption offset is the largest in this batch.
