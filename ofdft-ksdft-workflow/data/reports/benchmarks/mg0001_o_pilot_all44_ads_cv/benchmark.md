# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all44_adsorption_cv

- Truth records: 44
- Truth records with energy: 44

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 44 |  |  | 232.111 | 31.9407 | 0.113883 | no | 92.1424 | 63.9185 |
| dftpy_pbe_ads_delta_cv | 44 |  |  | 0.41768 | 0.418528 | 0.746723 | no | 92.1424 | 63.9185 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 44
- Candidate converged records: 44
- Matched records: 44
- Matched candidate converged records: 44
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 232.111
- adsorption_energy_raw_rmse_ev: 235.775
- adsorption_energy_raw_mean_signed_error_ev: 232.111
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 232.111
- adsorption_energy_aligned_mae_ev: 31.9407
- adsorption_energy_aligned_rmse_ev: 41.4004
- adsorption_energy_aligned_max_abs_error_ev: 98.9649
- adsorption_spearman_energy: 0.113883
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1303.66
- max_force_rmse_ev_per_ang: 1303.79
- candidate_runtime_median_seconds: 2.08156
- truth_runtime_median_seconds: 135.004
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 2d9196aa6d7e2257

### dftpy_pbe_ads_delta_cv

- Candidate records: 44
- Candidate converged records: 44
- Matched records: 44
- Matched candidate converged records: 44
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.41768
- adsorption_energy_raw_rmse_ev: 0.634689
- adsorption_energy_raw_mean_signed_error_ev: -0.0212079
- adsorption_energy_raw_max_abs_error_ev: 2.9748
- adsorption_energy_offset_ev: -0.0212079
- adsorption_energy_aligned_mae_ev: 0.418528
- adsorption_energy_aligned_rmse_ev: 0.634335
- adsorption_energy_aligned_max_abs_error_ev: 2.95359
- adsorption_spearman_energy: 0.746723
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1303.66
- max_force_rmse_ev_per_ang: 1303.79
- candidate_runtime_median_seconds: 2.08156
- truth_runtime_median_seconds: 135.004
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 2d9196aa6d7e2257
