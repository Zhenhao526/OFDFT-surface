# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12_cv

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_raw_cv | 12 | 539.329 | 48.1636 | -0.104895 | no | 25.6249 | 62.3109 |
| dftpy_pbe_delta_cv | 12 | 40.9573 | 39.1429 | -0.153846 | no | 25.6249 | 62.3109 |

## Details

### dftpy_pbe_raw_cv

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: -539.329
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.329
- energy_aligned_max_abs_error_ev: 103.629
- max_force_mae_ev_per_ang: 1307.11
- max_force_rmse_ev_per_ang: 1307.48
- candidate_runtime_median_seconds: 2.13328
- truth_runtime_median_seconds: 134.135
- Matched structure ids: 0173b205f6a5e0d7, 1b6f66e847adf264, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 76c2512dfce874bd, 7e0cb75306f47f6f, 9ed899052c1ede60, a2330293e814d720

### dftpy_pbe_delta_cv

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: 13.5142
- energy_raw_max_abs_error_ev: 141.327
- energy_offset_ev: 13.5142
- energy_aligned_max_abs_error_ev: 127.813
- max_force_mae_ev_per_ang: 1307.11
- max_force_rmse_ev_per_ang: 1307.48
- candidate_runtime_median_seconds: 2.13328
- truth_runtime_median_seconds: 134.135
- Matched structure ids: 0173b205f6a5e0d7, 1b6f66e847adf264, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 5d6c0ab5cb071bfa, 636c3943e12895cb, 76c2512dfce874bd, 7e0cb75306f47f6f, 9ed899052c1ede60, a2330293e814d720
