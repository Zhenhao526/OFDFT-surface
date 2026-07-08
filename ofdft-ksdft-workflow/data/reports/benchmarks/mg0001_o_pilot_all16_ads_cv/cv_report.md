# Delta Cross-Validation Report

- Truth name: `ksdft_qe_pbe_scf_pilot_all16_adsorption_cv`
- Usable records: 16
- Folds: 4 / requested 4
- Ridge alpha: 1.0
- Truth energy key: `ks_adsorption_energy_ev`
- Candidate energy key: `adsorption_energy_ev`
- Corrected energy key: `corrected_adsorption_energy_ev`

## Fold Summary

| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 12 | 4 | 0.290931 | 0.441379 | 0173b205f6a5e0d7, 26610f4a86dc91d1, 636c3943e12895cb, 9ed899052c1ede60 |
| 1 | 12 | 4 | 0.402282 | 0.498457 | 0aa0b2a8b9e7bb13, 3495ef2ffd6cb58f, 6abb28fe07b26672, a2330293e814d720 |
| 2 | 12 | 4 | 0.417688 | 0.462819 | 1b6f66e847adf264, 3d67f03958e4b24f, 76c2512dfce874bd, f67b4fe8525ec26c |
| 3 | 12 | 4 | 0.389579 | 0.493379 | 22438c289ddb70f3, 5d6c0ab5cb071bfa, 7e0cb75306f47f6f, fb75a97fd775c76d |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all16_adsorption_cv

- Truth records: 16
- Truth records with energy: 16

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 16 |  |  | 225.774 | 51.2764 | 0.0794118 | no | 33.8757 | 62.679 |
| dftpy_pbe_ads_delta_cv | 16 |  |  | 0.9571 | 0.968782 | 0.270588 | no | 33.8757 | 62.679 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 16
- Candidate converged records: 16
- Matched records: 16
- Matched candidate converged records: 16
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 225.774
- adsorption_energy_raw_rmse_ev: 233.056
- adsorption_energy_raw_mean_signed_error_ev: 225.774
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 225.774
- adsorption_energy_aligned_mae_ev: 51.2764
- adsorption_energy_aligned_rmse_ev: 57.8031
- adsorption_energy_aligned_max_abs_error_ev: 92.6271
- adsorption_spearman_energy: 0.0794118
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1308.68
- max_force_rmse_ev_per_ang: 1308.98
- candidate_runtime_median_seconds: 2.09981
- truth_runtime_median_seconds: 131.882
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 3d67f03958e4b24f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 6abb28fe07b26672

### dftpy_pbe_ads_delta_cv

- Candidate records: 16
- Candidate converged records: 16
- Matched records: 16
- Matched candidate converged records: 16
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.9571
- adsorption_energy_raw_rmse_ev: 1.38881
- adsorption_energy_raw_mean_signed_error_ev: -0.093461
- adsorption_energy_raw_max_abs_error_ev: 4.57265
- adsorption_energy_offset_ev: -0.093461
- adsorption_energy_aligned_mae_ev: 0.968782
- adsorption_energy_aligned_rmse_ev: 1.38566
- adsorption_energy_aligned_max_abs_error_ev: 4.47919
- adsorption_spearman_energy: 0.270588
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1308.68
- max_force_rmse_ev_per_ang: 1308.98
- candidate_runtime_median_seconds: 2.09981
- truth_runtime_median_seconds: 131.882
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 3d67f03958e4b24f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 6abb28fe07b26672
