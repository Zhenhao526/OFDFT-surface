# Delta Cross-Validation Report

- Truth name: `ksdft_qe_pbe_scf_pilot_all20_adsorption_cv`
- Usable records: 20
- Folds: 4 / requested 4
- Ridge alpha: 1.0
- Truth energy key: `ks_adsorption_energy_ev`
- Candidate energy key: `adsorption_energy_ev`
- Corrected energy key: `corrected_adsorption_energy_ev`

## Fold Summary

| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 15 | 5 | 0.315609 | 0.432672 | 0173b205f6a5e0d7, 26610f4a86dc91d1, 5d6c0ab5cb071bfa, 7dbf152ecbb0fdcb, ad9ffa908746cb59 |
| 1 | 15 | 5 | 0.387369 | 0.458834 | 0aa0b2a8b9e7bb13, 3495ef2ffd6cb58f, 636c3943e12895cb, 7e0cb75306f47f6f, d129ec3f37fc8539 |
| 2 | 15 | 5 | 0.334092 | 0.369956 | 1b6f66e847adf264, 3d67f03958e4b24f, 6abb28fe07b26672, 9ed899052c1ede60, f67b4fe8525ec26c |
| 3 | 15 | 5 | 0.384179 | 0.46822 | 22438c289ddb70f3, 46256f03336b7973, 76c2512dfce874bd, a2330293e814d720, fb75a97fd775c76d |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all20_adsorption_cv

- Truth records: 20
- Truth records with energy: 20

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 20 |  |  | 219.625 | 45.9397 | 0.0180451 | no | 42.2643 | 63.2504 |
| dftpy_pbe_ads_delta_cv | 20 |  |  | 0.959243 | 0.990275 | 0.299248 | no | 42.2643 | 63.2504 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 20
- Candidate converged records: 20
- Matched records: 20
- Matched candidate converged records: 20
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 219.625
- adsorption_energy_raw_rmse_ev: 225.982
- adsorption_energy_raw_mean_signed_error_ev: 219.625
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 219.625
- adsorption_energy_aligned_mae_ev: 45.9397
- adsorption_energy_aligned_rmse_ev: 53.2214
- adsorption_energy_aligned_max_abs_error_ev: 97.5655
- adsorption_spearman_energy: 0.0180451
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1308.83
- max_force_rmse_ev_per_ang: 1309.07
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 133.972
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 3d67f03958e4b24f, 46256f03336b7973, 5d6c0ab5cb071bfa, 636c3943e12895cb

### dftpy_pbe_ads_delta_cv

- Candidate records: 20
- Candidate converged records: 20
- Matched records: 20
- Matched candidate converged records: 20
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.959243
- adsorption_energy_raw_rmse_ev: 1.50497
- adsorption_energy_raw_mean_signed_error_ev: -0.166249
- adsorption_energy_raw_max_abs_error_ev: 5.58698
- adsorption_energy_offset_ev: -0.166249
- adsorption_energy_aligned_mae_ev: 0.990275
- adsorption_energy_aligned_rmse_ev: 1.49576
- adsorption_energy_aligned_max_abs_error_ev: 5.42073
- adsorption_spearman_energy: 0.299248
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1308.83
- max_force_rmse_ev_per_ang: 1309.07
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 133.972
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 3d67f03958e4b24f, 46256f03336b7973, 5d6c0ab5cb071bfa, 636c3943e12895cb
