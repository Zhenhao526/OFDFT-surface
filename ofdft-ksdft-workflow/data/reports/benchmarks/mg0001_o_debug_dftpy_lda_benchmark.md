# KSDFT Benchmark: ksdft_qe_pbe_debug

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_wt_debug | 12 | 532.802 | 50.8837 | 0.153846 | no | 21.5948 | 10.0113 |
| raw_fast | 12 | 23575.5 | 1.00242 | -0.664336 | no | 0.000218707 | 988502 |

## Details

### dftpy_lda_wt_debug

- Candidate records: 12
- Candidate converged records: 0
- Matched records: 12
- Matched candidate converged records: 0
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: 532.802
- energy_raw_max_abs_error_ev: 599.58
- energy_offset_ev: 532.802
- energy_aligned_max_abs_error_ev: 119.237
- max_force_mae_ev_per_ang: 1279.66
- max_force_rmse_ev_per_ang: 1280.86
- candidate_runtime_median_seconds: 1.77506
- truth_runtime_median_seconds: 17.4152
- Matched structure ids: d6956ca864e76798, d934123ad1c64e6c, a2a22756ea7d51da, 22a44412cf566eb8, cf3dec1024a17bba, 4dd34df24c37a67f, 17453818539e1161, af93973140fe595b, 4d00370b632fa437, 272134a217800bfb

### raw_fast

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: 23575.5
- energy_raw_max_abs_error_ev: 23577.5
- energy_offset_ev: 23575.5
- energy_aligned_max_abs_error_ev: 1.99596
- max_force_mae_ev_per_ang: 3.93533
- max_force_rmse_ev_per_ang: 4.19081
- candidate_runtime_median_seconds: 1.23961e-05
- truth_runtime_median_seconds: 17.4152
- Matched structure ids: d6956ca864e76798, d934123ad1c64e6c, a2a22756ea7d51da, 22a44412cf566eb8, cf3dec1024a17bba, 4dd34df24c37a67f, 17453818539e1161, af93973140fe595b, 4d00370b632fa437, 272134a217800bfb
