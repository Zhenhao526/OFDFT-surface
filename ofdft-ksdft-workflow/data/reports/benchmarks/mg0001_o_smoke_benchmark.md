# KSDFT Benchmark: ksdft_qe_pbe_smoke

- Truth records: 1
- Truth records with energy: 1

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| ksdft_self | 1 | 0 | 0 |  | yes | 15.198 | 1 |
| fake_fast | 1 | 23575.7 | 0 |  | yes | 5.9042e-05 | 257410 |

## Details

### ksdft_self

- Candidate records: 1
- Matched records: 1
- Energy pairs: 1
- energy_raw_mean_signed_error_ev: 0
- energy_raw_max_abs_error_ev: 0
- energy_offset_ev: 0
- energy_aligned_max_abs_error_ev: 0
- force_vector_mae_ev_per_ang: 0
- force_vector_rmse_ev_per_ang: 0
- max_force_mae_ev_per_ang: 0
- max_force_rmse_ev_per_ang: 0
- candidate_runtime_median_seconds: 15.198
- truth_runtime_median_seconds: 15.198
- Matched structure ids: 4dd34df24c37a67f

### fake_fast

- Candidate records: 1
- Matched records: 1
- Energy pairs: 1
- energy_raw_mean_signed_error_ev: 23575.7
- energy_raw_max_abs_error_ev: 23575.7
- energy_offset_ev: 23575.7
- energy_aligned_max_abs_error_ev: 0
- max_force_mae_ev_per_ang: 4.23088
- max_force_rmse_ev_per_ang: 4.23088
- candidate_runtime_median_seconds: 5.9042e-05
- truth_runtime_median_seconds: 15.198
- Matched structure ids: 4dd34df24c37a67f
