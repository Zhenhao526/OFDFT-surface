# KS-Anchor KEDF Adsorption Benchmark

This benchmark replaces the fixed absolute atomic-O reference with a per-KEDF effective oxygen chemical potential calibrated to one KSDFT adsorption anchor:

```text
Delta_i(KEDF) = E_KEDF(Mg slab + O_i) - E_KEDF(clean Mg slab)
mu_O_eff(KEDF) = Delta_anchor(KEDF) - E_ads_KS(anchor)
E_ads_pred(i) = Delta_i(KEDF) - mu_O_eff(KEDF)
```

This removes the inconsistent absolute O-energy zero from the mixed KEDF/M-OFDFT branch. The remaining first4 test checks whether the KEDF relative interface-energy landscape is physically usable.

## KS Anchor

- structure_id: `f67b4fe8525ec26c`
- truth adsorption key: `ks_adsorption_energy_ev`
- KS adsorption energy: `-4.61192` eV
- site/height: `top` / `2` A

## Effective mu_O

| variant | records | anchor Delta(eV) | KS anchor Eads(eV) | mu_O_eff(eV) |
| --- | ---: | ---: | ---: | ---: |
| `wt_heg_sp08_m30` | 4 | -594.261 | -4.61192 | -589.649 |
| `mgp_atomic_sp08_m30` | 4 | -727.899 | -4.61192 | -723.287 |
| `mgpa_atomic_sp08_m30` | 4 | -659.925 | -4.61192 | -655.313 |
| `lmgp_atomic_sp08_m30` | 4 | -459.417 | -4.61192 | -454.805 |
| `lmgpa_atomic_sp08_m30` | 4 | -429.901 | -4.61192 | -425.289 |
| `hc_atomic_sp08_m30` | 4 | -454.581 | -4.61192 | -449.969 |
| `revhc_atomic_sp08_m30` | 4 | -452.067 | -4.61192 | -447.455 |
| `tf_heg_sp08_m100` | 4 | -456.813 | -4.61192 | -452.201 |
| `tfvw_heg_sp08_m100` | 4 | -397.413 | -4.61192 | -392.801 |

## Adsorption Sign Sanity

For atomic O adsorption on Mg(0001), the KSDFT references in this benchmark are negative. The first4 branch is eligible for 12-structure expansion only when calibrated adsorption energies stay negative.

| variant | records | negative Eads | nonnegative Eads | min Eads(eV) | max Eads(eV) | first4 gate |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `wt_heg_sp08_m30` | 4 | 1 | 3 | -4.61192 | 133.556 | block 12 |
| `mgp_atomic_sp08_m30` | 4 | 1 | 3 | -4.61192 | 98.0144 | block 12 |
| `mgpa_atomic_sp08_m30` | 4 | 1 | 3 | -4.61192 | 115.532 | block 12 |
| `lmgp_atomic_sp08_m30` | 4 | 1 | 3 | -4.61192 | 37.7506 | block 12 |
| `lmgpa_atomic_sp08_m30` | 4 | 1 | 3 | -4.61192 | 27.9494 | block 12 |
| `hc_atomic_sp08_m30` | 4 | 1 | 3 | -4.61192 | 35.7496 | block 12 |
| `revhc_atomic_sp08_m30` | 4 | 1 | 3 | -4.61192 | 28.4091 | block 12 |
| `tf_heg_sp08_m100` | 4 | 1 | 3 | -4.61192 | 35.0556 | block 12 |
| `tfvw_heg_sp08_m100` | 4 | 1 | 3 | -4.61192 | 17.0193 | block 12 |

## Expansion Gate

- passed: `False`
- passed variants: `none`
- blocked variants: `wt_heg_sp08_m30, mgp_atomic_sp08_m30, mgpa_atomic_sp08_m30, lmgp_atomic_sp08_m30, lmgpa_atomic_sp08_m30, hc_atomic_sp08_m30, revhc_atomic_sp08_m30, tf_heg_sp08_m100, tfvw_heg_sp08_m100`
- decision: 12-structure expansion is blocked until the first4 sign sanity check passes.

## Benchmark

# KSDFT Benchmark: ksdft_anchored_mu_o

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| wt_heg_sp08_m30 | 4 | 568.249 | 37.1035 | 74.2069 | 37.1035 | 0.6 | no | 636.434 | 0.841417 |
| mgp_atomic_sp08_m30 | 4 | 70.8348 | 34.6305 | 69.2609 | 34.6305 | 0 | no | 716.615 | 0.747272 |
| mgpa_atomic_sp08_m30 | 4 | 142.264 | 35.6966 | 71.3932 | 35.6966 | 0 | no | 777.822 | 0.688469 |
| lmgp_atomic_sp08_m30 | 4 | 16955.1 | 14.2491 | 18.1903 | 14.2491 | 0 | no | 743.946 | 0.719819 |
| lmgpa_atomic_sp08_m30 | 4 | 18758.2 | 11.0287 | 14.4417 | 11.0287 | 0 | no | 510.26 | 1.04948 |
| hc_atomic_sp08_m30 | 4 | 17349 | 13.2822 | 17.6698 | 13.2822 | 0 | no | 540.139 | 0.991423 |
| revhc_atomic_sp08_m30 | 4 | 17508.5 | 9.60791 | 15.5001 | 9.60791 | 0 | no | 602.51 | 0.888792 |
| tf_heg_sp08_m100 | 4 | 17137.3 | 13.1686 | 15.3003 | 13.1686 | 0 | no | 1319.85 | 0.405734 |
| tfvw_heg_sp08_m100 | 4 | 21042.5 | 6.11634 | 12.2327 | 6.11634 | 0.6 | no | 473.859 | 1.1301 |

## Details

### wt_heg_sp08_m30

- Candidate records: 4
- Candidate converged records: 0
- Matched records: 4
- Matched candidate converged records: 0
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: -568.249
- energy_raw_max_abs_error_ev: 642.456
- energy_offset_ev: -568.249
- energy_aligned_max_abs_error_ev: 74.2069
- adsorption_energy_raw_mae_ev: 74.2069
- adsorption_energy_raw_rmse_ev: 88.9427
- adsorption_energy_raw_mean_signed_error_ev: 74.2069
- adsorption_energy_raw_max_abs_error_ev: 137.765
- adsorption_energy_offset_ev: 74.2069
- adsorption_energy_aligned_mae_ev: 37.1035
- adsorption_energy_aligned_rmse_ev: 49.032
- adsorption_energy_aligned_max_abs_error_ev: 74.2069
- adsorption_spearman_energy: 0.6
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 1333.47
- max_force_rmse_ev_per_ang: 1333.75
- candidate_runtime_median_seconds: 155.673
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### mgp_atomic_sp08_m30

- Candidate records: 4
- Candidate converged records: 0
- Matched records: 4
- Matched candidate converged records: 0
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 70.8348
- energy_raw_max_abs_error_ev: 103.797
- energy_offset_ev: 70.8348
- energy_aligned_max_abs_error_ev: 69.2609
- adsorption_energy_raw_mae_ev: 69.2609
- adsorption_energy_raw_rmse_ev: 80.7723
- adsorption_energy_raw_mean_signed_error_ev: 69.2609
- adsorption_energy_raw_max_abs_error_ev: 102.223
- adsorption_energy_offset_ev: 69.2609
- adsorption_energy_aligned_mae_ev: 34.6305
- adsorption_energy_aligned_rmse_ev: 41.5583
- adsorption_energy_aligned_max_abs_error_ev: 69.2609
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 1075.84
- max_force_rmse_ev_per_ang: 1076.16
- candidate_runtime_median_seconds: 179.085
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### mgpa_atomic_sp08_m30

- Candidate records: 4
- Candidate converged records: 0
- Matched records: 4
- Matched candidate converged records: 0
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: -142.264
- energy_raw_max_abs_error_ev: 213.657
- energy_offset_ev: -142.264
- energy_aligned_max_abs_error_ev: 71.3932
- adsorption_energy_raw_mae_ev: 71.3932
- adsorption_energy_raw_rmse_ev: 83.8761
- adsorption_energy_raw_mean_signed_error_ev: 71.3932
- adsorption_energy_raw_max_abs_error_ev: 119.741
- adsorption_energy_offset_ev: 71.3932
- adsorption_energy_aligned_mae_ev: 35.6966
- adsorption_energy_aligned_rmse_ev: 44.0252
- adsorption_energy_aligned_max_abs_error_ev: 71.3932
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 1198.56
- max_force_rmse_ev_per_ang: 1199.16
- candidate_runtime_median_seconds: 196.317
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### lmgp_atomic_sp08_m30

- Candidate records: 4
- Candidate converged records: 3
- Matched records: 4
- Matched candidate converged records: 3
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 16955.1
- energy_raw_max_abs_error_ev: 16978.9
- energy_offset_ev: 16955.1
- energy_aligned_max_abs_error_ev: 23.769
- adsorption_energy_raw_mae_ev: 18.1903
- adsorption_energy_raw_rmse_ev: 24.2282
- adsorption_energy_raw_mean_signed_error_ev: 18.1903
- adsorption_energy_raw_max_abs_error_ev: 41.9593
- adsorption_energy_offset_ev: 18.1903
- adsorption_energy_aligned_mae_ev: 14.2491
- adsorption_energy_aligned_rmse_ev: 16.0037
- adsorption_energy_aligned_max_abs_error_ev: 23.769
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 257.685
- max_force_rmse_ev_per_ang: 260.576
- candidate_runtime_median_seconds: 184.668
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### lmgpa_atomic_sp08_m30

- Candidate records: 4
- Candidate converged records: 0
- Matched records: 4
- Matched candidate converged records: 0
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 18758.2
- energy_raw_max_abs_error_ev: 18775.9
- energy_offset_ev: 18758.2
- energy_aligned_max_abs_error_ev: 17.7164
- adsorption_energy_raw_mae_ev: 14.4417
- adsorption_energy_raw_rmse_ev: 18.931
- adsorption_energy_raw_mean_signed_error_ev: 14.4417
- adsorption_energy_raw_max_abs_error_ev: 32.1582
- adsorption_energy_offset_ev: 14.4417
- adsorption_energy_aligned_mae_ev: 11.0287
- adsorption_energy_aligned_rmse_ev: 12.2401
- adsorption_energy_aligned_max_abs_error_ev: 17.7164
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 228.058
- max_force_rmse_ev_per_ang: 230.392
- candidate_runtime_median_seconds: 126.362
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### hc_atomic_sp08_m30

- Candidate records: 4
- Candidate converged records: 2
- Matched records: 4
- Matched candidate converged records: 2
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 17349
- energy_raw_max_abs_error_ev: 17371.3
- energy_offset_ev: 17349
- energy_aligned_max_abs_error_ev: 22.2886
- adsorption_energy_raw_mae_ev: 17.6698
- adsorption_energy_raw_rmse_ev: 23.2125
- adsorption_energy_raw_mean_signed_error_ev: 17.6698
- adsorption_energy_raw_max_abs_error_ev: 39.9583
- adsorption_energy_offset_ev: 17.6698
- adsorption_energy_aligned_mae_ev: 13.2822
- adsorption_energy_aligned_rmse_ev: 15.0532
- adsorption_energy_aligned_max_abs_error_ev: 22.2886
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 254.178
- max_force_rmse_ev_per_ang: 256.946
- candidate_runtime_median_seconds: 133.141
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### revhc_atomic_sp08_m30

- Candidate records: 4
- Candidate converged records: 2
- Matched records: 4
- Matched candidate converged records: 2
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 17508.5
- energy_raw_max_abs_error_ev: 17525.6
- energy_offset_ev: 17508.5
- energy_aligned_max_abs_error_ev: 17.1178
- adsorption_energy_raw_mae_ev: 15.5001
- adsorption_energy_raw_rmse_ev: 19.4454
- adsorption_energy_raw_mean_signed_error_ev: 15.5001
- adsorption_energy_raw_max_abs_error_ev: 32.6178
- adsorption_energy_offset_ev: 15.5001
- adsorption_energy_aligned_mae_ev: 9.60791
- adsorption_energy_aligned_rmse_ev: 11.7418
- adsorption_energy_aligned_max_abs_error_ev: 17.1178
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 230.258
- max_force_rmse_ev_per_ang: 231.975
- candidate_runtime_median_seconds: 148.058
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### tf_heg_sp08_m100

- Candidate records: 4
- Candidate converged records: 4
- Matched records: 4
- Matched candidate converged records: 4
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 17137.3
- energy_raw_max_abs_error_ev: 17161.3
- energy_offset_ev: 17137.3
- energy_aligned_max_abs_error_ev: 23.964
- adsorption_energy_raw_mae_ev: 15.3003
- adsorption_energy_raw_rmse_ev: 21.6346
- adsorption_energy_raw_mean_signed_error_ev: 15.3003
- adsorption_energy_raw_max_abs_error_ev: 39.2643
- adsorption_energy_offset_ev: 15.3003
- adsorption_energy_aligned_mae_ev: 13.1686
- adsorption_energy_aligned_rmse_ev: 15.2956
- adsorption_energy_aligned_max_abs_error_ev: 23.964
- adsorption_spearman_energy: 0
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 232.527
- max_force_rmse_ev_per_ang: 236.235
- candidate_runtime_median_seconds: 328.728
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

### tfvw_heg_sp08_m100

- Candidate records: 4
- Candidate converged records: 4
- Matched records: 4
- Matched candidate converged records: 4
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 21042.5
- energy_raw_max_abs_error_ev: 21051.5
- energy_offset_ev: 21042.5
- energy_aligned_max_abs_error_ev: 12.2327
- adsorption_energy_raw_mae_ev: 12.2327
- adsorption_energy_raw_rmse_ev: 14.4428
- adsorption_energy_raw_mean_signed_error_ev: 12.2327
- adsorption_energy_raw_max_abs_error_ev: 21.2281
- adsorption_energy_offset_ev: 12.2327
- adsorption_energy_aligned_mae_ev: 6.11634
- adsorption_energy_aligned_rmse_ev: 7.67827
- adsorption_energy_aligned_max_abs_error_ev: 12.2327
- adsorption_spearman_energy: 0.6
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 229.911
- max_force_rmse_ev_per_ang: 230.539
- candidate_runtime_median_seconds: 118.018
- truth_runtime_median_seconds: 133.176
- Matched structure ids: f67b4fe8525ec26c, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d

