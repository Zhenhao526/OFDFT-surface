# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot

- Truth records: 2
- Truth records with energy: 2

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_raw | 2 | 635.89 | 7.06869 | -1 | no | 4.15888 | 68.067 |
| dftpy_pbe_delta | 2 | 65.2601 | 65.2601 | 1 | yes | 4.15888 | 68.067 |

## Details

### dftpy_pbe_raw

- Candidate records: 2
- Candidate converged records: 2
- Matched records: 2
- Matched candidate converged records: 2
- Energy pairs: 2
- energy_raw_mean_signed_error_ev: -635.89
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -635.89
- energy_aligned_max_abs_error_ev: 7.06869
- max_force_mae_ev_per_ang: 1358.28
- max_force_rmse_ev_per_ang: 1359.17
- candidate_runtime_median_seconds: 2.07944
- truth_runtime_median_seconds: 141.541
- Matched structure ids: a2330293e814d720, f67b4fe8525ec26c

### dftpy_pbe_delta

- Candidate records: 2
- Candidate converged records: 2
- Matched records: 2
- Matched candidate converged records: 2
- Energy pairs: 2
- energy_raw_mean_signed_error_ev: 9.03009
- energy_raw_max_abs_error_ev: 74.2902
- energy_offset_ev: 9.03009
- energy_aligned_max_abs_error_ev: 65.2601
- max_force_mae_ev_per_ang: 1358.28
- max_force_rmse_ev_per_ang: 1359.17
- candidate_runtime_median_seconds: 2.07944
- truth_runtime_median_seconds: 141.541
- Matched structure ids: a2330293e814d720, f67b4fe8525ec26c
