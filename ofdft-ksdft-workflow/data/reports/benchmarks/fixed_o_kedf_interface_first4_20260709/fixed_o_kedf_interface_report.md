# Fixed Atomic-O KEDF Interface Benchmark

This benchmark uses one calibrated atomic-O reference for every KEDF variant:

```text
E_ads = E_KEDF(Mg slab + O) - E_KEDF(clean Mg slab) - E_fixed(O)
```

The goal is to focus the comparison on the adsorbed Mg+O and clean-slab KEDF energies after the atomic-O reference has been fixed.

Caveat: current KEDF coverage is still sparse. Four-structure pilot metrics are useful for screening obvious failures and offsets, but ranking conclusions require more completed slab+adsorbed pairs.

Physical sign sanity matters: for atomic O adsorption on Mg(0001), stable KSDFT reference adsorption energies in this benchmark are negative. A raw fixed-O KEDF branch that predicts nonnegative adsorption energies should be treated as a nonphysical diagnostic branch rather than a deployable adsorption-energy model.

## Adsorbate Reference

- reference_id: `o_atom_mldft_str25_qm9_pseudo_calibrated_to_qe_o_atom`
- total_energy_ev: `-559.8598218127081`

## Adsorption Sign Sanity

| variant | records | negative Eads | nonnegative Eads | min Eads(eV) | max Eads(eV) | sign check |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `wt_heg_sp08_m30` | 4 | 1 | 3 | -34.4008 | 103.767 | nonphysical raw branch |
| `mgp_atomic_sp08_m30` | 4 | 4 | 0 | -168.04 | -65.4133 | pass |
| `mgpa_atomic_sp08_m30` | 4 | 3 | 1 | -100.065 | 20.0786 | nonphysical raw branch |
| `lmgp_atomic_sp08_m30` | 4 | 0 | 4 | 100.443 | 142.805 | nonphysical raw branch |
| `lmgpa_atomic_sp08_m30` | 4 | 0 | 4 | 129.959 | 162.52 | nonphysical raw branch |
| `hc_atomic_sp08_m30` | 4 | 0 | 4 | 105.279 | 145.641 | nonphysical raw branch |
| `revhc_atomic_sp08_m30` | 4 | 0 | 4 | 107.793 | 140.814 | nonphysical raw branch |
| `tfvw_heg_sp08_m100` | 4 | 0 | 4 | 162.447 | 184.078 | nonphysical raw branch |
| `tf_heg_sp08_m100` | 4 | 0 | 4 | 103.047 | 142.714 | nonphysical raw branch |

Warning: at least one variant has nonnegative raw adsorption energies. Keep the benchmark metrics for diagnostics, but do not interpret this raw fixed-O/M-OFDFT mixed-reference branch as physical adsorption energies without an additional chemical-potential or KS-anchor calibration.

## Benchmark

# KSDFT Benchmark: ksdft_fixed_o

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| wt_heg_sp08_m30 | 4 | 568.249 | 37.1035 | 59.3124 | 37.1035 | 0.6 | no | 636.434 | 0.841417 |
| mgp_atomic_sp08_m30 | 4 | 70.8348 | 34.6305 | 94.1668 | 34.6305 | 0 | no | 716.615 | 0.747272 |
| mgpa_atomic_sp08_m30 | 4 | 142.264 | 35.6966 | 36.204 | 35.6966 | 0 | no | 777.822 | 0.688469 |
| lmgp_atomic_sp08_m30 | 4 | 16955.1 | 14.2491 | 123.245 | 14.2491 | 0 | no | 743.946 | 0.719819 |
| lmgpa_atomic_sp08_m30 | 4 | 18758.2 | 11.0287 | 149.012 | 11.0287 | 0 | no | 510.26 | 1.04948 |
| hc_atomic_sp08_m30 | 4 | 17349 | 13.2822 | 127.561 | 13.2822 | 0 | no | 540.139 | 0.991423 |
| revhc_atomic_sp08_m30 | 4 | 17508.5 | 9.60791 | 127.905 | 9.60791 | 0 | no | 602.51 | 0.888792 |
| tfvw_heg_sp08_m100 | 4 | 21042.5 | 6.11634 | 179.292 | 6.11634 | 0.6 | no | 473.859 | 1.1301 |
| tf_heg_sp08_m100 | 4 | 17137.3 | 13.1686 | 122.959 | 13.1686 | 0 | no | 1319.85 | 0.405734 |

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
- adsorption_energy_raw_mae_ev: 59.3124
- adsorption_energy_raw_rmse_ev: 66.1596
- adsorption_energy_raw_mean_signed_error_ev: 44.418
- adsorption_energy_raw_max_abs_error_ev: 107.976
- adsorption_energy_offset_ev: 44.418
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
- adsorption_energy_raw_mae_ev: 94.1668
- adsorption_energy_raw_rmse_ev: 102.929
- adsorption_energy_raw_mean_signed_error_ev: -94.1668
- adsorption_energy_raw_max_abs_error_ev: 163.428
- adsorption_energy_offset_ev: -94.1668
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
- adsorption_energy_raw_mae_ev: 36.204
- adsorption_energy_raw_rmse_ev: 50.1709
- adsorption_energy_raw_mean_signed_error_ev: -24.0604
- adsorption_energy_raw_max_abs_error_ev: 95.4536
- adsorption_energy_offset_ev: -24.0604
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
- adsorption_energy_raw_mae_ev: 123.245
- adsorption_energy_raw_rmse_ev: 124.28
- adsorption_energy_raw_mean_signed_error_ev: 123.245
- adsorption_energy_raw_max_abs_error_ev: 147.014
- adsorption_energy_offset_ev: 123.245
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
- adsorption_energy_raw_mae_ev: 149.012
- adsorption_energy_raw_rmse_ev: 149.514
- adsorption_energy_raw_mean_signed_error_ev: 149.012
- adsorption_energy_raw_max_abs_error_ev: 166.729
- adsorption_energy_offset_ev: 149.012
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
- adsorption_energy_raw_mae_ev: 127.561
- adsorption_energy_raw_rmse_ev: 128.446
- adsorption_energy_raw_mean_signed_error_ev: 127.561
- adsorption_energy_raw_max_abs_error_ev: 149.849
- adsorption_energy_offset_ev: 127.561
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
- adsorption_energy_raw_mae_ev: 127.905
- adsorption_energy_raw_rmse_ev: 128.443
- adsorption_energy_raw_mean_signed_error_ev: 127.905
- adsorption_energy_raw_max_abs_error_ev: 145.023
- adsorption_energy_offset_ev: 127.905
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
- adsorption_energy_raw_mae_ev: 179.292
- adsorption_energy_raw_rmse_ev: 179.456
- adsorption_energy_raw_mean_signed_error_ev: 179.292
- adsorption_energy_raw_max_abs_error_ev: 188.287
- adsorption_energy_offset_ev: 179.292
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
- adsorption_energy_raw_mae_ev: 122.959
- adsorption_energy_raw_rmse_ev: 123.906
- adsorption_energy_raw_mean_signed_error_ev: 122.959
- adsorption_energy_raw_max_abs_error_ev: 146.923
- adsorption_energy_offset_ev: 122.959
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

