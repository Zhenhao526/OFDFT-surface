# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12_adsorption

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads | 12 | 539.329 | 48.1636 | 236.776 | 48.1636 | -0.104895 | no | 25.6249 | 62.3109 |
| dftpy_lda_ads | 12 | 417.251 | 48.1004 | 230.955 | 48.1004 | -0.104895 | no | 23.1428 | 68.9937 |

## Details

### dftpy_pbe_ads

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: -539.329
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.329
- energy_aligned_max_abs_error_ev: 103.629
- adsorption_energy_raw_mae_ev: 236.776
- adsorption_energy_raw_rmse_ev: 243.419
- adsorption_energy_raw_mean_signed_error_ev: 236.776
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 236.776
- adsorption_energy_aligned_mae_ev: 48.1636
- adsorption_energy_aligned_rmse_ev: 56.4792
- adsorption_energy_aligned_max_abs_error_ev: 103.629
- adsorption_spearman_energy: -0.104895
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1307.11
- max_force_rmse_ev_per_ang: 1307.48
- candidate_runtime_median_seconds: 2.13328
- truth_runtime_median_seconds: 134.135
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f

### dftpy_lda_ads

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: -417.251
- energy_raw_max_abs_error_ev: 520.4
- energy_offset_ev: -417.251
- energy_aligned_max_abs_error_ev: 103.148
- adsorption_energy_raw_mae_ev: 230.955
- adsorption_energy_raw_rmse_ev: 237.743
- adsorption_energy_raw_mean_signed_error_ev: 230.955
- adsorption_energy_raw_max_abs_error_ev: 312.024
- adsorption_energy_offset_ev: 230.955
- adsorption_energy_aligned_mae_ev: 48.1004
- adsorption_energy_aligned_rmse_ev: 56.402
- adsorption_energy_aligned_max_abs_error_ev: 103.148
- adsorption_spearman_energy: -0.104895
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1264.21
- max_force_rmse_ev_per_ang: 1264.59
- candidate_runtime_median_seconds: 1.89917
- truth_runtime_median_seconds: 134.135
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
