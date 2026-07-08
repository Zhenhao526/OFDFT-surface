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
| 0 | 9 | 3 | 0.380582 | 0.47282 | 0173b205f6a5e0d7, 5d6c0ab5cb071bfa, 9ed899052c1ede60 |
| 1 | 9 | 3 | 0.475263 | 0.529083 | 1b6f66e847adf264, 636c3943e12895cb, a2330293e814d720 |
| 2 | 9 | 3 | 0.367378 | 0.463856 | 26610f4a86dc91d1, 76c2512dfce874bd, f67b4fe8525ec26c |
| 3 | 9 | 3 | 0.430913 | 0.504741 | 3495ef2ffd6cb58f, 7e0cb75306f47f6f, fb75a97fd775c76d |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12_adsorption_cv

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 12 |  |  | 236.776 | 48.1636 | -0.104895 | no | 25.6249 | 62.3109 |
| dftpy_pbe_ads_delta_cv | 12 |  |  | 1.55864 | 1.68979 | 0.300699 | no | 25.6249 | 62.3109 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 0
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
- Matched structure ids: 0173b205f6a5e0d7, 1b6f66e847adf264, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 76c2512dfce874bd, 7e0cb75306f47f6f, 9ed899052c1ede60, a2330293e814d720

### dftpy_pbe_ads_delta_cv

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 1.55864
- adsorption_energy_raw_rmse_ev: 2.91818
- adsorption_energy_raw_mean_signed_error_ev: -0.647775
- adsorption_energy_raw_max_abs_error_ev: 9.61858
- adsorption_energy_offset_ev: -0.647775
- adsorption_energy_aligned_mae_ev: 1.68979
- adsorption_energy_aligned_rmse_ev: 2.84537
- adsorption_energy_aligned_max_abs_error_ev: 8.9708
- adsorption_spearman_energy: 0.300699
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1307.11
- max_force_rmse_ev_per_ang: 1307.48
- candidate_runtime_median_seconds: 2.13328
- truth_runtime_median_seconds: 134.135
- Matched structure ids: 0173b205f6a5e0d7, 1b6f66e847adf264, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 76c2512dfce874bd, 7e0cb75306f47f6f, 9ed899052c1ede60, a2330293e814d720
