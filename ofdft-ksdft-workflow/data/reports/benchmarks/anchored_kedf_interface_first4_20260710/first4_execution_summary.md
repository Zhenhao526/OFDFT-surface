# First4 KS-Anchor KEDF Diagnostic Summary

## Scope

- System: Mg(0001)+O, first 4 pilot adsorbed structures.
- Structures: top 1.6 A, top 2.0 A, top 2.4 A, bridge 1.6 A.
- Truth: `data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl`.
- Adsorbed KEDF records: `data/reports/benchmarks/remote_kedf_adsorbed_first4_libxc_20260709_1101`.
- Clean slab KEDF references: `data/reports/benchmarks/remote_kedf_references_20260708_151019` and `data/reports/benchmarks/remote_kedf_missing_refs_libxc_20260709_1055`.
- KS anchor: `f67b4fe8525ec26c`, top site, 2.0 A, `E_ads_KS = -4.611918940703731 eV`.

## Calibration Formula

```text
Delta_i(KEDF) = E_KEDF(Mg slab + O_i) - E_KEDF(clean Mg slab)
mu_O_eff(KEDF) = Delta_anchor(KEDF) - E_ads_KS(anchor)
E_ads_pred(i) = Delta_i(KEDF) - mu_O_eff(KEDF)
```

This branch removes the inconsistent absolute atomic-O reference from the fixed-O/M-OFDFT mixed-reference attempt. It tests whether each KEDF has a usable relative interface-energy landscape after a single KS adsorption anchor fixes the oxygen chemical potential.

## First4 Sign Sanity

The first4 gate fails for every KEDF variant. Each variant reproduces the anchor by construction, but the other three first4 structures become nonnegative adsorption energies.

| KEDF variant | records | negative Eads | nonnegative Eads | max Eads(eV) | first4 gate |
| --- | ---: | ---: | ---: | ---: | --- |
| `wt_heg_sp08_m30` | 4 | 1 | 3 | 133.556 | block 12 |
| `mgp_atomic_sp08_m30` | 4 | 1 | 3 | 98.014 | block 12 |
| `mgpa_atomic_sp08_m30` | 4 | 1 | 3 | 115.532 | block 12 |
| `lmgp_atomic_sp08_m30` | 4 | 1 | 3 | 37.751 | block 12 |
| `lmgpa_atomic_sp08_m30` | 4 | 1 | 3 | 27.949 | block 12 |
| `hc_atomic_sp08_m30` | 4 | 1 | 3 | 35.750 | block 12 |
| `revhc_atomic_sp08_m30` | 4 | 1 | 3 | 28.409 | block 12 |
| `tf_heg_sp08_m100` | 4 | 1 | 3 | 35.056 | block 12 |
| `tfvw_heg_sp08_m100` | 4 | 1 | 3 | 17.019 | block 12 |

## Error Ranking

Ranked by raw adsorption MAE after KS-anchor `mu_O_eff` calibration.

| rank | KEDF variant | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | runtime total (s) |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `tfvw_heg_sp08_m100` | 12.233 | 6.116 | 0.6 | 473.859 |
| 2 | `lmgpa_atomic_sp08_m30` | 14.442 | 11.029 | 0.0 | 510.260 |
| 3 | `tf_heg_sp08_m100` | 15.300 | 13.169 | 0.0 | 1319.847 |
| 4 | `revhc_atomic_sp08_m30` | 15.500 | 9.608 | 0.0 | 602.510 |
| 5 | `hc_atomic_sp08_m30` | 17.670 | 13.282 | 0.0 | 540.139 |
| 6 | `lmgp_atomic_sp08_m30` | 18.190 | 14.249 | 0.0 | 743.946 |
| 7 | `mgp_atomic_sp08_m30` | 69.261 | 34.630 | 0.0 | 716.615 |
| 8 | `mgpa_atomic_sp08_m30` | 71.393 | 35.697 | 0.0 | 777.822 |
| 9 | `wt_heg_sp08_m30` | 74.207 | 37.103 | 0.6 | 636.434 |

## Decision

- Do not expand this anchored branch to 12 structures yet.
- The sign failure is no longer an absolute-O reference problem: the per-KEDF `mu_O_eff` calibration fixes the energy zero at the anchor, but the relative KEDF interface-energy differences across first4 are still too large and produce nonphysical positive adsorption energies.
- The most informative next diagnostic is an anchor-sensitivity or leave-one-anchor-out check on first4, followed by a tighter subset of KEDF settings only if a physically motivated anchor choice passes the sign gate.
