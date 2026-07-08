# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all28_adsorption_cv

- Truth records: 28
- Truth records with energy: 28

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 28 |  |  | 222.248 | 37.004 | 0.114943 | no | 58.7924 | 64.2327 |
| dftpy_pbe_ads_delta_cv | 28 |  |  | 0.567106 | 0.568062 | 0.487137 | no | 58.7924 | 64.2327 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 28
- Candidate converged records: 28
- Matched records: 28
- Matched candidate converged records: 28
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 222.248
- adsorption_energy_raw_rmse_ev: 227.174
- adsorption_energy_raw_mean_signed_error_ev: 222.248
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 222.248
- adsorption_energy_aligned_mae_ev: 37.004
- adsorption_energy_aligned_rmse_ev: 47.0523
- adsorption_energy_aligned_max_abs_error_ev: 94.9431
- adsorption_spearman_energy: 0.114943
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1306.72
- max_force_rmse_ev_per_ang: 1306.9
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.66
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 306ad89390cf1f45, 3495ef2ffd6cb58f, 3d67f03958e4b24f, 3e94dc98e10574a6, 46256f03336b7973

### dftpy_pbe_ads_delta_cv

- Candidate records: 28
- Candidate converged records: 28
- Matched records: 28
- Matched candidate converged records: 28
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.567106
- adsorption_energy_raw_rmse_ev: 0.821801
- adsorption_energy_raw_mean_signed_error_ev: -0.00668849
- adsorption_energy_raw_max_abs_error_ev: 2.60872
- adsorption_energy_offset_ev: -0.00668849
- adsorption_energy_aligned_mae_ev: 0.568062
- adsorption_energy_aligned_rmse_ev: 0.821774
- adsorption_energy_aligned_max_abs_error_ev: 2.60203
- adsorption_spearman_energy: 0.487137
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 1306.72
- max_force_rmse_ev_per_ang: 1306.9
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.66
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 306ad89390cf1f45, 3495ef2ffd6cb58f, 3d67f03958e4b24f, 3e94dc98e10574a6, 46256f03336b7973
