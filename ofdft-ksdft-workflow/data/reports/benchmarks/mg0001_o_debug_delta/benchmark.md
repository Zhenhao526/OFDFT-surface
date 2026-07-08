# KSDFT Benchmark: ksdft_qe_pbe_debug

- Truth records: 5
- Truth records with energy: 5

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| raw_fast | 5 | 23575.3 | 1.05751 | -0.9 | no | 7.22908e-05 | 1.28191e+06 |
| delta_corrected | 5 | 1.29406 | 1.22037 | -0.2 | no | 7.22908e-05 | 1.28191e+06 |

## Details

### raw_fast

- Candidate records: 5
- Matched records: 5
- Energy pairs: 5
- energy_raw_mean_signed_error_ev: 23575.3
- energy_raw_max_abs_error_ev: 23577.5
- energy_offset_ev: 23575.3
- energy_aligned_max_abs_error_ev: 2.16637
- max_force_mae_ev_per_ang: 3.49049
- max_force_rmse_ev_per_ang: 3.57199
- candidate_runtime_median_seconds: 1.2416e-05
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c

### delta_corrected

- Candidate records: 5
- Matched records: 5
- Energy pairs: 5
- energy_raw_mean_signed_error_ev: -0.36847
- energy_raw_max_abs_error_ev: 1.93949
- energy_offset_ev: -0.36847
- energy_aligned_max_abs_error_ev: 2.18433
- max_force_mae_ev_per_ang: 3.49049
- max_force_rmse_ev_per_ang: 3.57199
- candidate_runtime_median_seconds: 1.2416e-05
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c
