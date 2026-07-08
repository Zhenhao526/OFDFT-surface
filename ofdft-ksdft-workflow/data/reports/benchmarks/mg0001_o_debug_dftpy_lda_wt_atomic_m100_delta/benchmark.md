# KSDFT Benchmark: ksdft_qe_pbe_debug

- Truth records: 5
- Truth records with energy: 5

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_wt_atomic_m100_raw | 5 | 527.486 | 58.5113 | 0.7 | no | 9.4915 | 9.76351 |
| dftpy_lda_wt_atomic_m100_delta | 5 | 1.60498 | 1.55447 | -0.5 | no | 9.4915 | 9.76351 |

## Details

### dftpy_lda_wt_atomic_m100_raw

- Candidate records: 5
- Candidate converged records: 5
- Matched records: 5
- Matched candidate converged records: 5
- Energy pairs: 5
- energy_raw_mean_signed_error_ev: 527.486
- energy_raw_max_abs_error_ev: 597.132
- energy_offset_ev: 527.486
- energy_aligned_max_abs_error_ev: 113.561
- max_force_mae_ev_per_ang: 1268.75
- max_force_rmse_ev_per_ang: 1269.77
- candidate_runtime_median_seconds: 1.89991
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c

### dftpy_lda_wt_atomic_m100_delta

- Candidate records: 5
- Candidate converged records: 5
- Matched records: 5
- Matched candidate converged records: 5
- Energy pairs: 5
- energy_raw_mean_signed_error_ev: -0.25252
- energy_raw_max_abs_error_ev: 2.26701
- energy_offset_ev: -0.25252
- energy_aligned_max_abs_error_ev: 2.14984
- max_force_mae_ev_per_ang: 1268.75
- max_force_rmse_ev_per_ang: 1269.77
- candidate_runtime_median_seconds: 1.89991
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c
