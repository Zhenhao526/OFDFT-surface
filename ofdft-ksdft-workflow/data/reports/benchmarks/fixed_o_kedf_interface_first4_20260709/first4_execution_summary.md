# First4 Fixed-O KEDF Diagnostic Summary

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

## Adsorption Sign Sanity

The direct fixed-O mixed-reference branch fails the basic physical sign check for most variants. For atomic O adsorption on Mg(0001), the KSDFT truth values in this benchmark are negative. Nonnegative predicted adsorption energies mean this raw branch should not be interpreted as a physical adsorption-energy model.

| KEDF variant | matched | negative Eads | nonnegative Eads | sign check |
| --- | ---: | ---: | ---: | --- |
| `mgp_atomic_sp08_m30` | 4 | 4 | 0 | pass |
| `mgpa_atomic_sp08_m30` | 4 | 3 | 1 | fail |
| `wt_heg_sp08_m30` | 4 | 1 | 3 | fail |
| `lmgp_atomic_sp08_m30` | 4 | 0 | 4 | fail |
| `lmgpa_atomic_sp08_m30` | 4 | 0 | 4 | fail |
| `hc_atomic_sp08_m30` | 4 | 0 | 4 | fail |
| `revhc_atomic_sp08_m30` | 4 | 0 | 4 | fail |
| `tf_heg_sp08_m100` | 4 | 0 | 4 | fail |
| `tfvw_heg_sp08_m100` | 4 | 0 | 4 | fail |

## Diagnostic Error Ranking

Ranked by raw adsorption MAE against KSDFT. This table is diagnostic only because the raw fixed-O/M-OFDFT mixed-reference branch is not physically valid for variants with nonnegative adsorption energies.

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

- The direct fixed-O absolute-reference route is not acceptable as a production adsorption-energy definition. Eight of nine variants produce at least one nonnegative adsorption energy on a system where the KSDFT references are negative.
- The formula sign is not reversed: `E_ads = E(slab+O) - E(slab) - E(O)` is correct. The problem is that the calibrated M-OFDFT atomic-O absolute energy is being mixed with KEDF slab and interface energies that do not share a consistent energy zero.
- Raw adsorption MAE is still large for every KEDF. MGP is the only variant that passes the sign check on these four structures, but its raw MAE remains 94.167 eV, so passing the sign check alone is not enough.
- Several methods have small aligned MAE after removing a constant adsorption offset, especially TFvW, revHC, LMGPA, TF, HC, and LMGP. This suggests the relative shape may contain useful information, but only after explicit offset or chemical-potential calibration.
- Spearman is mostly 0 with only 4 structures. Treat ranking/top-k metrics as diagnostic only.
- Runtime totals include four adsorbed calculations plus one clean slab reference per variant. These fresh remote timings were collected on a busy login node and should not replace a controlled speed benchmark.

## Next Step

Do not promote the raw fixed-O mixed-reference branch directly to 12-structure production. First build a calibrated adsorption-energy branch:

- Calibrate an effective `mu_O` or adsorption offset per KEDF using a KSDFT anchor structure.
- Recompute first4 adsorption energies after calibration and require the sign sanity check to pass.
- Only then expand promising variants to 12 structures, likely starting with `mgp_atomic_sp08_m30`, `mgpa_atomic_sp08_m30`, `wt_heg_sp08_m30`, `revhc_atomic_sp08_m30`, `hc_atomic_sp08_m30`, and `lmgp_atomic_sp08_m30`.
