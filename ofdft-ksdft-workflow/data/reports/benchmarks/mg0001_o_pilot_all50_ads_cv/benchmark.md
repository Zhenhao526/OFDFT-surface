# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all50_adsorption_cv

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 50 |  |  | 236.127 | 31.5988 | 0.152845 | no | 104.76 | 63.7136 |
| dftpy_pbe_ads_delta_cv | 50 |  |  | 0.325418 | 0.325418 | 0.827323 | no | 104.76 | 63.7136 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 50
- Candidate converged records: 50
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 236.127
- adsorption_energy_raw_rmse_ev: 239.552
- adsorption_energy_raw_mean_signed_error_ev: 236.127
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 236.127
- adsorption_energy_aligned_mae_ev: 31.5988
- adsorption_energy_aligned_rmse_ev: 40.3647
- adsorption_energy_aligned_max_abs_error_ev: 102.98
- adsorption_spearman_energy: 0.152845
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- candidate_runtime_median_seconds: 2.08225
- truth_runtime_median_seconds: 133.27
- Matched structure ids: 0173b205f6a5e0d7, 0199c00b22820d26, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 2086432d65d5b674, 22438c289ddb70f3

### dftpy_pbe_ads_delta_cv

- Candidate records: 50
- Candidate converged records: 50
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.325418
- adsorption_energy_raw_rmse_ev: 0.424436
- adsorption_energy_raw_mean_signed_error_ev: -0.0187516
- adsorption_energy_raw_max_abs_error_ev: 1.58132
- adsorption_energy_offset_ev: -0.0187516
- adsorption_energy_aligned_mae_ev: 0.325418
- adsorption_energy_aligned_rmse_ev: 0.424021
- adsorption_energy_aligned_max_abs_error_ev: 1.56257
- adsorption_spearman_energy: 0.827323
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- candidate_runtime_median_seconds: 2.08225
- truth_runtime_median_seconds: 133.27
- Matched structure ids: 0173b205f6a5e0d7, 0199c00b22820d26, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 2086432d65d5b674, 22438c289ddb70f3
