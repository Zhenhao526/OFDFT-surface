# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all36_adsorption_cv

- Truth records: 36
- Truth records with energy: 36

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 36 |  |  | 227.584 | 33.9922 | 0.150837 | no | 75.4577 | 64.1885 |
| dftpy_pbe_ads_delta_cv | 36 |  |  | 0.466502 | 0.484067 | 0.643243 | no | 75.4577 | 64.1885 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 36
- Candidate converged records: 36
- Matched records: 36
- Matched candidate converged records: 36
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 227.584
- adsorption_energy_raw_rmse_ev: 231.889
- adsorption_energy_raw_mean_signed_error_ev: 227.584
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 227.584
- adsorption_energy_aligned_mae_ev: 33.9922
- adsorption_energy_aligned_rmse_ev: 44.4736
- adsorption_energy_aligned_max_abs_error_ev: 94.4375
- adsorption_spearman_energy: 0.150837
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1304.5
- max_force_rmse_ev_per_ang: 1304.65
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.511
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 306ad89390cf1f45, 32673556c4a07276, 3495ef2ffd6cb58f, 3d67f03958e4b24f

### dftpy_pbe_ads_delta_cv

- Candidate records: 36
- Candidate converged records: 36
- Matched records: 36
- Matched candidate converged records: 36
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.466502
- adsorption_energy_raw_rmse_ev: 0.697126
- adsorption_energy_raw_mean_signed_error_ev: -0.104773
- adsorption_energy_raw_max_abs_error_ev: 3.01183
- adsorption_energy_offset_ev: -0.104773
- adsorption_energy_aligned_mae_ev: 0.484067
- adsorption_energy_aligned_rmse_ev: 0.689207
- adsorption_energy_aligned_max_abs_error_ev: 2.90706
- adsorption_spearman_energy: 0.643243
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1304.5
- max_force_rmse_ev_per_ang: 1304.65
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.511
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 306ad89390cf1f45, 32673556c4a07276, 3495ef2ffd6cb58f, 3d67f03958e4b24f
