# KSDFT Benchmark: ksdft_qe_pbe_debug_adsorption

- Truth records: 5
- Truth records with energy: 5

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw | 5 | 249.867 | 59.6052 | 0.7 | no | 9.69222 | 9.56131 |
| dftpy_pbe_ads_delta | 5 | 1.53272 | 1.47413 | -0.5 | no | 9.69222 | 9.56131 |

## Details

### dftpy_pbe_ads_raw

- Candidate records: 5
- Candidate converged records: 5
- Matched records: 5
- Matched candidate converged records: 5
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 249.867
- adsorption_energy_raw_rmse_ev: 258.908
- adsorption_energy_raw_mean_signed_error_ev: 249.867
- adsorption_energy_raw_max_abs_error_ev: 320.856
- adsorption_energy_offset_ev: 249.867
- adsorption_energy_aligned_mae_ev: 59.6052
- adsorption_energy_aligned_rmse_ev: 67.823
- adsorption_energy_aligned_max_abs_error_ev: 116.359
- adsorption_spearman_energy: 0.7
- adsorption_top1_match: no
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 1311.03
- max_force_rmse_ev_per_ang: 1312.58
- candidate_runtime_median_seconds: 1.91586
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c

### dftpy_pbe_ads_delta

- Candidate records: 5
- Candidate converged records: 5
- Matched records: 5
- Matched candidate converged records: 5
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 1.53272
- adsorption_energy_raw_rmse_ev: 1.63597
- adsorption_energy_raw_mean_signed_error_ev: -0.292984
- adsorption_energy_raw_max_abs_error_ev: 2.23339
- adsorption_energy_offset_ev: -0.292984
- adsorption_energy_aligned_mae_ev: 1.47413
- adsorption_energy_aligned_rmse_ev: 1.60952
- adsorption_energy_aligned_max_abs_error_ev: 2.13252
- adsorption_spearman_energy: -0.5
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1311.03
- max_force_rmse_ev_per_ang: 1312.58
- candidate_runtime_median_seconds: 1.91586
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c
