# Delta Cross-Validation Report

- Truth name: `ksdft_qe_pbe_scf_pilot_all12_adsorption_cv`
- Usable records: 12
- Folds: 4 / requested 4
- Ridge alpha: 1.0
- Truth energy key: `ks_adsorption_energy_ev`
- Candidate energy key: `adsorption_energy_ev`
- Corrected energy key: `corrected_adsorption_energy_ev`

## Fold Summary

| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 9 | 3 | 0.382381 | 0.481451 | 0173b205f6a5e0d7, 5d6c0ab5cb071bfa, 9ed899052c1ede60 |
| 1 | 9 | 3 | 0.494566 | 0.548059 | 1b6f66e847adf264, 636c3943e12895cb, a2330293e814d720 |
| 2 | 9 | 3 | 0.387088 | 0.446732 | 26610f4a86dc91d1, 76c2512dfce874bd, f67b4fe8525ec26c |
| 3 | 9 | 3 | 0.434986 | 0.510451 | 3495ef2ffd6cb58f, 7e0cb75306f47f6f, fb75a97fd775c76d |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12_adsorption_cv

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_ads_raw_cv | 12 |  |  | 230.955 | 48.1004 | -0.104895 | no | 23.1428 | 68.9937 |
| dftpy_lda_ads_delta_cv | 12 |  |  | 1.9054 | 2.098 | 0.195804 | no | 23.1428 | 68.9937 |

## Details

### dftpy_lda_ads_raw_cv

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 0
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
- Matched structure ids: 0173b205f6a5e0d7, 1b6f66e847adf264, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 76c2512dfce874bd, 7e0cb75306f47f6f, 9ed899052c1ede60, a2330293e814d720

### dftpy_lda_ads_delta_cv

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 1.9054
- adsorption_energy_raw_rmse_ev: 3.94807
- adsorption_energy_raw_mean_signed_error_ev: -1.02265
- adsorption_energy_raw_max_abs_error_ev: 13.3081
- adsorption_energy_offset_ev: -1.02265
- adsorption_energy_aligned_mae_ev: 2.098
- adsorption_energy_aligned_rmse_ev: 3.81333
- adsorption_energy_aligned_max_abs_error_ev: 12.2855
- adsorption_spearman_energy: 0.195804
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1264.21
- max_force_rmse_ev_per_ang: 1264.59
- candidate_runtime_median_seconds: 1.89917
- truth_runtime_median_seconds: 134.135
- Matched structure ids: 0173b205f6a5e0d7, 1b6f66e847adf264, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 76c2512dfce874bd, 7e0cb75306f47f6f, 9ed899052c1ede60, a2330293e814d720
